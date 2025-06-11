from surge import Report
from surge.errors import SurgeRequestError
from unittest import mock
import pytest


def test_save_report_on_empty_project_raises_an_error():
    with mock.patch.object(Report, "post") as mock_post:
        mock_post.return_value = {"error": "Project has no responses"}
        with pytest.raises(SurgeRequestError):
            Report.save_report("fake_project_id", "export_csv",
                               "my_report.csv")
