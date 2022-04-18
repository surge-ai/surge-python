from surge.errors import SurgeMissingIDError, SurgeMissingAttributeError
from surge.api_resource import REPORTS_ENDPOINT, APIResource


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
    def request(cls, project_id: str, type: str):
        '''
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
        '''
        endpoint = f"{REPORTS_ENDPOINT}/{project_id}/report"
        params = {"report_type": type}
        response_json = cls.post(endpoint, params)
        return cls(**response_json)

    @classmethod
    def status(cls, project_id: str, job_id: str):
        '''
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
        '''
        endpoint = f"{REPORTS_ENDPOINT}/{project_id}/report_status"
        params = {"job_id": job_id}
        response_json = cls.get(endpoint, params)
        return cls(**response_json)
