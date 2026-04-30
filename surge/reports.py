import gzip
from time import sleep, monotonic
import urllib
import tempfile
import shutil
import io
import json
import warnings

from surge.api_resource import REPORTS_ENDPOINT, APIResource
from surge.errors import SurgeRequestError


class Report(APIResource):

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)

    def __str__(self):
        return f"<surge.Report>"

    def __repr__(self):
        return f"<surge.Report {self.attrs_repr()}>"

    def attrs_repr(self):
        return self.print_attrs(forbid_list=["id"])

    @classmethod
    def save_report(
        cls,
        project_id: str,
        type: str,
        filepath=None,
        poll_time=5 * 60,
        api_key: str = None,
        poll_interval: float = 2,
    ):
        """
        Request creation of a report, poll until the report is generated, and save the data to a file all in one call.

        Calls ``request`` once to start (or reuse) a generation job and
        then polls ``check_status`` against the returned ``job_id``
        until that specific job finishes. Polling a specific job —
        rather than re-calling ``request`` in a loop — avoids
        re-triggering generation on projects that are still receiving
        responses, which would otherwise cause this call to hang.

        Arguments:
            project_id (string): UUID of project to get data for
            type (string): Must be one of these types:
              * `export_json`
              * `export_json_aggregated`
              * `export_csv`
              * `export_csv_aggregated`
              * `export_csv_flattened`
            filepath (string or IO or None): Location to save the results file. If not specified, will save to "project_{project_id}_results.{csv/json}
            poll_time (int): Maximum number of seconds to wait for the report to be generated
            poll_interval (int or float): Seconds to wait between status checks
        """
        response = cls.request(project_id=project_id,
                               type=type,
                               api_key=api_key)
        deadline = monotonic() + poll_time
        while response.status in ("CREATING", "IN_PROGRESS", "RETRYING"):
            if monotonic() >= deadline:
                raise Exception(
                    "Report failed to generate within {poll_time} seconds".
                    format(poll_time=poll_time))
            sleep(poll_interval)
            response = cls.check_status(project_id,
                                        response.job_id,
                                        api_key=api_key)

        if response.status not in ("READY", "COMPLETED"):
            raise ValueError("Report failed to generate with status {}".format(
                response.status))

        file_ext = "csv" if "csv" in type else "json"
        default_file_name = "project_{project_id}_results.{file_ext}".format(
            project_id=project_id, file_ext=file_ext)
        target = filepath or default_file_name
        with urllib.request.urlopen(response.url) as remote:
            with tempfile.NamedTemporaryFile() as tmp_file:
                shutil.copyfileobj(remote, tmp_file)
                tmp_file.flush()
                data = gzip.open(tmp_file.name, "r").read()
        if isinstance(target, str):
            with open(target, "wb") as f:
                f.write(data)
        else:
            target.write(data)
        return data

    @classmethod
    def download_json(cls,
                      project_id: str,
                      poll_time=5 * 60,
                      api_key: str = None):
        """
        Download and parse the results JSON for a project

        Arguments:
            project_id (string): UUID of project to get data for
            poll_time (int): Number of seconds to poll for the report

        Returns:
            results (list): List of dictionaries of results for each response
        """
        bytesio = io.BytesIO()
        cls.save_report(
            project_id=project_id,
            type="export_json",
            filepath=bytesio,
            poll_time=poll_time,
            api_key=api_key,
        )
        bytesio.seek(0)
        return json.load(bytesio)

    @classmethod
    def request(cls, project_id: str, type: str, api_key: str = None):
        """
        Request creation of a report for the given type. Note that reports are generated
        asychronously so the response may include a `job_id` which needs to be used with
        the `status` method to get the job status. In the event that the report has is
        already generated and current, the report URL will be returned. Note that the URL
        is a presigned URL which is active for only a limited duration.

        Type may be one of these types:
          * `export_json`
          * `export_json_aggregated`
          * `export_csv`
          * `export_csv_aggregated`
          * `export_csv_flattened`

        These are the different responses:

        1) The report is being generated:

          {
            status: "CREATING",
            job_id: ...,
          }

        2) The report is already generated and up to date:

          {
            status: "READY",
            url: ...,
            expires_in_seconds: ...,
          }

        Arguments:
            project_id (str): ID of project.
            report_type (str): report type

        Returns:
            status: Report status object which includes report id
        """
        endpoint = f"{REPORTS_ENDPOINT}/{project_id}/report"
        params = {"report_type": type}
        response_json = cls.post(endpoint, params, api_key=api_key)
        if "error" in response_json:
            raise SurgeRequestError(response_json["error"])
        return cls(**response_json)

    @classmethod
    def status(cls, project_id: str, job_id: str, api_key: str = None):
        """
        Deprecated (use `check_status` instead). Checks the status of a given report job. The response will be of one of these shapes:

        1) Report is still being generated (HTTP 202):

          {
            status: "IN_PROGRESS",
          }

        2) Report is completed:

          {
            status: "COMPLETED",
            url: ...,
            expires_in_seconds: ...,
          }

        3) Retrying generation of report (can consider this to be same as in progress):

          {
            status: "RETRYING",
            job_id: ...,
          }

        4) Error (HTTP 400 or 500):

          {
            status: "ERROR",
            type: ...
          }

        Arguments:
          project_id (str): ID of project.
          job_id (str): ID of the report job

        Returns:
            status: Report status object
        """
        warnings.warn("Use check_status instead", DeprecationWarning)
        return cls.check_status(project_id, job_id, api_key=api_key)

    @classmethod
    def check_status(cls, project_id: str, job_id: str, api_key: str = None):
        """
        Checks the status of a given report job. The response will be of one of these shapes:

        1) Report is still being generated (HTTP 202):

          {
            status: "IN_PROGRESS",
          }

        2) Report is completed:

          {
            status: "COMPLETED",
            url: ...,
            expires_in_seconds: ...,
          }

        3) Retrying generation of report (can consider this to be same as in progress):

          {
            status: "RETRYING",
            job_id: ...,
          }

        4) Error (HTTP 400 or 500):

          {
            status: "ERROR",
            type: ...
          }

        Arguments:
          project_id (str): ID of project.
          job_id (str): ID of the report job

        Returns:
            status: Report status object
        """
        endpoint = f"{REPORTS_ENDPOINT}/{project_id}/report_status"
        params = {"job_id": job_id}
        response_json = cls.get(endpoint, params, api_key=api_key)
        return cls(**response_json)
