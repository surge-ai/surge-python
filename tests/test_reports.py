import gzip
import io
from surge import Report
from surge.errors import SurgeRequestError
from unittest import mock
import pytest


def _gzipped(payload: bytes) -> bytes:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
        gz.write(payload)
    return buf.getvalue()


def test_save_report_on_empty_project_raises_an_error():
    with mock.patch.object(Report, "post") as mock_post:
        mock_post.return_value = {"error": "Project has no responses"}
        with pytest.raises(SurgeRequestError):
            Report.save_report("fake_project_id", "export_csv",
                               "my_report.csv")


def test_save_report_downloads_when_request_returns_ready():
    """If request returns READY, no polling is needed."""
    payload = b'[{"a": 1}]'
    ready = Report(status="READY", url="https://signed.example/report.gz")
    sink = io.BytesIO()
    with mock.patch.object(Report, "request",
                           return_value=ready) as mock_request, \
            mock.patch.object(Report, "check_status") as mock_check, \
            mock.patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = io.BytesIO(
            _gzipped(payload))
        Report.save_report("proj-123", "export_json", filepath=sink)
    mock_request.assert_called_once()
    mock_check.assert_not_called()
    assert sink.getvalue() == payload


def test_save_report_polls_check_status_for_returned_job_id():
    """When request returns CREATING, poll check_status against that job_id.

    IN_PROGRESS responses from check_status do not include a job_id —
    we have to remember the one from the initial CREATING response
    rather than re-reading it on each iteration.
    """
    payload = b"a,b\n1,2\n"
    creating = Report(status="CREATING", job_id="job-abc")
    in_progress = Report(status="IN_PROGRESS")
    completed = Report(status="COMPLETED",
                       url="https://signed.example/report.gz")
    sink = io.BytesIO()
    with mock.patch.object(Report, "request",
                           return_value=creating) as mock_request, \
            mock.patch.object(Report, "check_status",
                              side_effect=[in_progress, completed]) as mock_check, \
            mock.patch("urllib.request.urlopen") as mock_urlopen, \
            mock.patch("surge.reports.sleep") as mock_sleep:
        mock_urlopen.return_value.__enter__.return_value = io.BytesIO(
            _gzipped(payload))
        Report.save_report("proj-123", "export_csv", filepath=sink)
    mock_request.assert_called_once()
    assert mock_check.call_count == 2
    for call in mock_check.call_args_list:
        assert call.args[:2] == ("proj-123", "job-abc")
    assert mock_sleep.call_count == 2
    assert sink.getvalue() == payload


def test_save_report_switches_job_id_on_retrying():
    """RETRYING responses include a new job_id; subsequent polls use it."""
    payload = b'[]'
    creating = Report(status="CREATING", job_id="job-abc")
    retrying = Report(status="RETRYING", job_id="job-xyz")
    in_progress = Report(status="IN_PROGRESS")
    completed = Report(status="COMPLETED",
                       url="https://signed.example/report.gz")
    sink = io.BytesIO()
    with mock.patch.object(Report, "request", return_value=creating), \
            mock.patch.object(Report, "check_status",
                              side_effect=[retrying, in_progress, completed]) as mock_check, \
            mock.patch("urllib.request.urlopen") as mock_urlopen, \
            mock.patch("surge.reports.sleep"):
        mock_urlopen.return_value.__enter__.return_value = io.BytesIO(
            _gzipped(payload))
        Report.save_report("proj-123", "export_json", filepath=sink)
    job_ids = [call.args[1] for call in mock_check.call_args_list]
    assert job_ids == ["job-abc", "job-xyz", "job-xyz"]


def test_save_report_raises_on_unexpected_status():
    creating = Report(status="CREATING", job_id="job-abc")
    error = Report(status="ERROR", type="Report generation error")
    with mock.patch.object(Report, "request", return_value=creating), \
            mock.patch.object(Report, "check_status", return_value=error), \
            mock.patch("surge.reports.sleep"):
        with pytest.raises(ValueError, match="ERROR"):
            Report.save_report("proj-123",
                               "export_json",
                               filepath=io.BytesIO())


def test_save_report_times_out_when_job_never_completes():
    creating = Report(status="CREATING", job_id="job-abc")
    in_progress = Report(status="IN_PROGRESS", job_id="job-abc")
    with mock.patch.object(Report, "request", return_value=creating), \
            mock.patch.object(Report, "check_status",
                              return_value=in_progress), \
            mock.patch("surge.reports.sleep"), \
            mock.patch("surge.reports.monotonic",
                       side_effect=[0.0, 1000.0, 2000.0]):
        with pytest.raises(Exception, match="within 300 seconds"):
            Report.save_report("proj-123",
                               "export_json",
                               filepath=io.BytesIO())
