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
    with (
            mock.patch.object(Report, "request", return_value=ready) as
            mock_request,
            mock.patch.object(Report, "check_status") as mock_check,
            mock.patch("urllib.request.urlopen") as mock_urlopen,
    ):
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
    with (
            mock.patch.object(Report, "request",
                              return_value=creating) as mock_request,
            mock.patch.object(Report,
                              "check_status",
                              side_effect=[in_progress, completed]) as
            mock_check,
            mock.patch("urllib.request.urlopen") as mock_urlopen,
            mock.patch("time.sleep") as mock_sleep,
    ):
        mock_urlopen.return_value.__enter__.return_value = io.BytesIO(
            _gzipped(payload))
        Report.save_report("proj-123", "export_csv", filepath=sink)
    mock_request.assert_called_once()
    assert mock_check.call_count == 2
    for call in mock_check.call_args_list:
        assert call.args[:2] == ("proj-123", "job-abc")
    assert mock_sleep.call_count == 1
    assert sink.getvalue() == payload


def test_save_report_switches_job_id_on_retrying():
    """RETRYING responses include a new job_id; subsequent polls use it."""
    payload = b"[]"
    creating = Report(status="CREATING", job_id="job-abc")
    retrying = Report(status="RETRYING", job_id="job-xyz")
    in_progress = Report(status="IN_PROGRESS")
    completed = Report(status="COMPLETED",
                       url="https://signed.example/report.gz")
    sink = io.BytesIO()
    with (
            mock.patch.object(Report, "request", return_value=creating),
            mock.patch.object(Report,
                              "check_status",
                              side_effect=[retrying, in_progress, completed])
            as mock_check,
            mock.patch("urllib.request.urlopen") as mock_urlopen,
            mock.patch("time.sleep"),
    ):
        mock_urlopen.return_value.__enter__.return_value = io.BytesIO(
            _gzipped(payload))
        Report.save_report("proj-123", "export_json", filepath=sink)
    job_ids = [call.args[1] for call in mock_check.call_args_list]
    assert job_ids == ["job-abc", "job-xyz", "job-xyz"]


def test_save_report_raises_on_unexpected_status():
    creating = Report(status="CREATING", job_id="job-abc")
    error = Report(status="ERROR", type="Report generation error")
    with (
            mock.patch.object(Report, "request", return_value=creating),
            mock.patch.object(Report, "check_status", return_value=error),
            mock.patch("time.sleep"),
    ):
        with pytest.raises(ValueError, match="ERROR"):
            Report.save_report("proj-123",
                               "export_json",
                               filepath=io.BytesIO())


def test_save_report_times_out_when_job_never_completes():
    creating = Report(status="CREATING", job_id="job-abc")
    in_progress = Report(status="IN_PROGRESS", job_id="job-abc")
    with (
            mock.patch.object(Report, "request", return_value=creating),
            mock.patch.object(Report, "check_status",
                              return_value=in_progress),
            mock.patch("time.sleep"),
            mock.patch("time.monotonic", side_effect=[0.0, 1000.0, 2000.0]),
    ):
        with pytest.raises(Exception, match="within 300 seconds"):
            Report.save_report("proj-123",
                               "export_json",
                               filepath=io.BytesIO())


def test_request_merges_extra_params_into_post_body():
    with mock.patch.object(Report, "post") as mock_post:
        mock_post.return_value = {"status": "CREATING", "job_id": "j"}
        Report.request("proj-1", "export_json", extra_params={"item_id": "i"})
    endpoint, params = mock_post.call_args.args[:2]
    assert "report" in endpoint
    assert params == {"report_type": "export_json", "item_id": "i"}


def test_request_without_extra_params_sends_only_report_type():
    with mock.patch.object(Report, "post") as mock_post:
        mock_post.return_value = {"status": "CREATING", "job_id": "j"}
        Report.request("proj-1", "export_json")
    _, params = mock_post.call_args.args[:2]
    assert params == {"report_type": "export_json"}


def test_save_report_raises_when_initial_request_returns_error():
    """If request() returns ERROR directly, raise without polling check_status."""
    error = Report(status="ERROR", type="Report generation error")
    with (
            mock.patch.object(Report, "request", return_value=error),
            mock.patch.object(Report, "check_status") as mock_check,
    ):
        with pytest.raises(ValueError, match="ERROR"):
            Report.save_report("proj-e", "export_json", filepath=io.BytesIO())
    mock_check.assert_not_called()


def test_save_report_treats_completed_initial_response_as_terminal():
    """If request() returns COMPLETED (not just READY), skip polling."""
    payload = b"[]"
    completed = Report(status="COMPLETED",
                       url="https://signed.example/report.gz")
    sink = io.BytesIO()
    with (
            mock.patch.object(Report, "request", return_value=completed) as
            mock_request,
            mock.patch.object(Report, "check_status") as mock_check,
            mock.patch("urllib.request.urlopen") as mock_urlopen,
    ):
        mock_urlopen.return_value.__enter__.return_value = io.BytesIO(
            _gzipped(payload))
        Report.save_report("proj-c", "export_json", filepath=sink)
    mock_request.assert_called_once()
    mock_check.assert_not_called()
    assert sink.getvalue() == payload


def test_request_rejects_report_type_in_extra_params():
    """report_type is set via the `type` argument; allowing it in
    extra_params would silently override the explicit `type`."""
    with mock.patch.object(Report, "post") as mock_post:
        with pytest.raises(ValueError, match="report_type"):
            Report.request("proj-1",
                           "export_csv",
                           extra_params={"report_type": "export_json"})
    mock_post.assert_not_called()


def test_save_report_forwards_extra_params_to_request():
    payload = b"[]"
    ready = Report(status="READY", url="https://signed.example/report.gz")
    with (
            mock.patch.object(Report, "request", return_value=ready) as
            mock_request,
            mock.patch("urllib.request.urlopen") as mock_urlopen,
    ):
        mock_urlopen.return_value.__enter__.return_value = io.BytesIO(
            _gzipped(payload))
        Report.save_report(
            "proj-1",
            "export_json",
            filepath=io.BytesIO(),
            extra_params={"item_id": "i"},
        )
    assert mock_request.call_args.kwargs["extra_params"] == {"item_id": "i"}
