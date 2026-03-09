from typing import List
import dateutil.parser
import datetime
import json

from surge.errors import (
    SurgeMissingIDError,
    SurgeProjectQuestionError,
    SurgeMissingAttributeError,
)
from surge.api_resource import PROJECTS_ENDPOINT, APIResource
from surge.questions import Question
from surge.reports import Report
from surge.tasks import Task
from surge import utils


class Project(APIResource):

    Question = Question
    Report = Report
    Task = Task

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)

        if self.id is None:
            raise SurgeMissingIDError

        if not (hasattr(self, "name") and self.name):
            raise SurgeMissingAttributeError

        if hasattr(self, "created_at") and self.created_at:
            # Convert timestamp str into datetime
            self.created_at = dateutil.parser.parse(self.created_at)

        # If the Project has Questions, convert each into a Question object
        if hasattr(self, "questions"):
            self.questions = self._convert_questions_to_objects(self.questions)

    def __str__(self):
        return f'<surge.Project#{self.id} name="{self.name}">'

    def __repr__(self):
        return f'<surge.Project#{self.id} name="{self.name}" {self.attrs_repr()}>'

    def attrs_repr(self):
        return self.print_attrs(forbid_list=["name", "id"])

    def _convert_questions_to_objects(self, questions_data):
        return list(
            map(lambda params: self.Question.from_params(params),
                questions_data))

    def to_dict(self):
        return {
            key: self._to_dict_value(key, value)
            for key, value in self.__dict__.items() if not key.startswith("_")
        }

    def _to_dict_value(self, key, value):
        if key == "questions":
            return [item.to_dict() for item in value if item]
        elif isinstance(value, datetime.datetime):
            return value.isoformat()
        else:
            return value

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def _validate_questions(questions):
        # Convert list of question objects into dicts in valid json format
        # If this isn't a list of Question objects, throw an exception
        if not all(isinstance(q, Question) for q in questions):
            raise SurgeProjectQuestionError

    @classmethod
    def create(
        cls,
        name: str,
        payment_per_response: float = None,
        private_workforce: bool = False,
        instructions: str = None,
        questions: list = None,
        qualifications_required: list = None,
        teams_required: list = None,
        teams_forbidden: list = None,
        callback_url: str = None,
        fields_template: str = None,
        num_workers_per_task: int = 1,
        tags=None,
        carousel=None,
        template_id: str = None,
        description: str = None,
        params: dict = None,
        api_key: str = None,
    ):
        """
        Creates a new Project.

        Arguments:
            name (str): Name of the project.
            payment_per_response (float, optional):
                How much a worker is paid (in US dollars) for an individual response.
            private_workforce (bool, optional):
                Indicates if the project's tasks will be done by a private workforce.
            instructions (str, optional): Instructions shown to workers describing how they should complete the task.
            questions (list, optional): An array of question objects describing the questions to be answered.
            qualifications_required (list, optional): Deprecated in favor of teams_required.
            teams_required (list, optional): If you have created custom teams, you can pass a list of team ids Surgers must have to work on the project here.
            teams_forbidden (list, optional): If you have created custom teams, you can pass a list of team ids Surgers must not have to work on the project here.
            callback_url (str, optional): url that receives a POST request with the project's data.
            fields_template (str, optional): A template describing how fields are shown to workers working on the task.
                For example, if fields_template is "{{company_name}}", then workers will be shown a link to the company.
            num_workers_per_task (int, optional): How many workers work on each task (i.e., how many responses per task).
            tags (list, optional): An array of strings to tag the project with. Worker won't see these tags.
            carousel (dict, optional): Advanced options for creating a carousel project.
            template_id (str, optional): ID of project to copy from. If you are using a template, you can omit all other parameters besides the name of the copy.
        Returns:
            project: new Project object
        """

        # Initialize mutable defaults to avoid shared state between calls
        if questions is None:
            questions = []
        if qualifications_required is None:
            qualifications_required = []
        if teams_required is None:
            teams_required = []
        if teams_forbidden is None:
            teams_forbidden = []
        if tags is None:
            tags = []
        if params is None:
            params = {}

        Project._validate_questions(questions)

        questions_json = [q.to_dict() for q in questions]

        # qualifications_required still needs to work for backwards
        # compatibility
        if len(teams_required) == 0 and len(qualifications_required) > 0:
            teams_required = qualifications_required

        params = {
            "name": name,
            "private_workforce": private_workforce,
            "instructions": instructions,
            "questions": questions_json,
            "qualifications_required": teams_required,
            "qualifications_forbidden": teams_forbidden,
            "callback_url": callback_url,
            "fields_template": fields_template,
            "num_workers_per_task": num_workers_per_task,
            "tags": tags,
            "description": description,
            **params,
        }
        if carousel is not None:
            params = {**params, **carousel.to_dict()}
        if payment_per_response is not None:
            params["payment_per_response"] = payment_per_response
        if template_id is not None:
            params["template_id"] = template_id
        response_json = cls.post(PROJECTS_ENDPOINT, params, api_key=api_key)
        return cls(**response_json)

    @classmethod
    def list(cls,
             page: int = 1,
             statuses: List[str] = None,
             api_key: str = None):
        """
        Lists all projects you have created.
        Projects are returned in descending order of created_at.
        Each page contains a maximum of 100 projects.

        Arguments:
            page (int, optional): Page number to retrieve. Pages start at 1 (default value).

        Returns:
            projects (list): list of Project objects.
        """
        params = {"page": page}
        if statuses:
            params["statuses[]"] = statuses
        response_json = cls.get(PROJECTS_ENDPOINT, params, api_key=api_key)
        projects = [cls(**project_json) for project_json in response_json]
        return projects

    @classmethod
    def list_shared(cls,
                    page: int = 1,
                    statuses: List[str] = None,
                    api_key: str = None):
        """
        Lists all projects created by anyone in your organization.
        Projects are returned in descending order of created_at.
        Each page contains a maximum of 100 projects.

        Arguments:
            page (int, optional): Page number to retrieve. Pages start at 1 (default value).

        Returns:
            projects (list): list of Project objects.
        """
        params = {"page": page}
        if statuses:
            params["statuses[]"] = statuses
        endpoint = f"{PROJECTS_ENDPOINT}/shared"
        response_json = cls.get(endpoint, params, api_key=api_key)
        projects = [cls(**project_json) for project_json in response_json]
        return projects

    @classmethod
    def list_blueprints(cls, page: int = 1, api_key: str = None):
        """
        Lists blueprint projects for your organization.

        Returns:
            projects (list): list of Project objects.
        """
        params = {"page": page}
        endpoint = f"{PROJECTS_ENDPOINT}/blueprints"
        response_json = cls.get(endpoint, params, api_key=api_key)
        projects = [cls(**project_json) for project_json in response_json]
        return projects

    @classmethod
    def retrieve(cls, project_id: str, api_key: str = None):
        """
        Retrieves a specific project you have created.

        Arguments:
            project_id (str): ID of project.

        Returns:
            project: Project object
        """
        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}"
        response_json = cls.get(endpoint, api_key=api_key)
        return cls(**response_json)

    def list_copies(self, api_key: str = None):
        """
        Lists copies made from the current project.

        Returns:
            projects (list): list of Project objects.
        """
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/copies"
        response_json = self.get(endpoint, api_key=api_key)
        projects = [self.__class__(**project_json) for project_json in response_json]
        return projects

    def launch(self, api_key: str = None):
        """
        Launches a project.
        If work is being completed by the Surge workforce, you will be charged when the project launches
        and your accounts neeeds to have sufficient funds before launching.

        Returns:
            project: new Project object with updated status
        """
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/launch"
        return self.put(endpoint, api_key=api_key)

    def pause(self, api_key: str = None):
        """
        Pauses a project.
        Tasks added to the project will not be worked on until you resume the project.

        Returns:
            project: new Project object with updated status
        """
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/pause"
        return self.put(endpoint, api_key=api_key)

    def resume(self, api_key: str = None):
        """
        Resumes a paused project.

        Returns:
            project: new Project object with updated status
        """
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/resume"
        return self.put(endpoint, api_key=api_key)

    def cancel(self, api_key: str = None):
        """
        Cancels a project.

        Returns:
            project: new Project object with updated status
        """
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/cancel"
        return self.put(endpoint, api_key=api_key)

    def delete(self, api_key: str = None):
        """
        Permanently delete the project, including the input data and all responses.

        Returns:
            {"success": True}
        """
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/delete"
        return self.get(endpoint, api_key=api_key)

    def list_tasks(self,
                   page: int = 1,
                   per_page: int = 100,
                   api_key: str = None):
        """
        Lists all tasks belonging to this project.
        Tasks are returned in ascending order of created_at.
        Each page contains a maximum of 25 tasks.

        Arguments:
            page (int, optional): Page number to retrieve. Pages start at 1 (default value).

        Returns:
            tasks (list): list of Task objects.
        """
        return self.Task.list(self.id,
                              page=page,
                              per_page=per_page,
                              api_key=api_key)

    def create_tasks(self,
                     tasks_data: list,
                     launch=False,
                     api_key: str = None):
        """
        Creates new Task objects for this project.

        Arguments:
            tasks_data (list): list of dicts that map each task field to its value
                e.g. [{"website": "surgehq.ai"}, {"website":"twitch.tv"}]

        Returns:
            tasks (list): list of Task objects
        """
        return self.Task.create_many(self.id,
                                     tasks_data,
                                     launch,
                                     api_key=api_key)

    def create_tasks_from_csv(self, file_path: str, api_key: str = None):
        """
        Creates new Task objects for this project from a local CSV file.
        The header of the CSV file must specify the fields that are used in your Tasks.

        Arguments:
            file_path (str): path to CSV file.

        Returns:
            tasks (list): list of Task objects
        """
        tasks_data = utils.load_tasks_data_from_csv(file_path)
        return self.create_tasks(tasks_data, api_key=api_key)

    def update(
        self,
        name: str = None,
        payment_per_response: float = None,
        instructions: str = None,
        callback_url: str = None,
        fields_template: str = None,
        num_workers_per_task: int = 0,
        description: str = None,
        params: dict = None,
        api_key: str = None,
    ):
        """
        Update an existing project

        Arguments:
            name (str): Name of the project.
            payment_per_response (float, optional):
                How much a worker is paid (in US dollars) for an individual response.
            instructions (str, optional): Instructions shown to workers describing how they should complete the task.
            callback_url (str, optional): url that receives a POST request with the project's data.
            fields_template (str, optional): A template describing how fields are shown to workers working on the task.
                For example, if fields_template is "{{company_name}}", then workers will be shown a link to the company.
            num_workers_per_task (int, optional): How many workers work on each task (i.e., how many responses per task).

        Returns:
            project: new Project object
        """

        if params is None:
            params = {}
        params = {**params}

        if name is not None and len(name) > 0:
            params["name"] = name
        if payment_per_response is not None:
            params["payment_per_response"] = payment_per_response
        if instructions is not None and len(instructions) > 0:
            params["instructions"] = instructions
        if description is not None and len(description) > 0:
            params["description"] = description
        if callback_url is not None and len(callback_url) > 0:
            params["callback_url"] = callback_url
        if fields_template is not None and len(fields_template) > 0:
            params["fields_text"] = fields_template
        if num_workers_per_task > 0:
            params["num_workers_per_task"] = num_workers_per_task

        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}"
        response_json = self.put(endpoint, params, api_key=api_key)
        return self.__class__(**response_json)

    def workable_by_surger(self, surger_id, api_key: str = None):
        """
        Checks if a specific Surger can work on this project.

        Arguments:
            surger_id (str): ID of surger.

        Returns:
            workable (bool): True if surger can work on this project, False otherwise.
        """
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/workable_by_surger"
        params = {"surger_id": surger_id}
        response_json = self.get(endpoint, params, api_key=api_key)
        return response_json.get("workable", False)

    def save_report(
        self,
        type: str,
        filepath=None,
        poll_time=5 * 60,
        api_key: str = None,
    ):
        """
        Request creation of a report, poll until the report is generated, and save the data to a file all in one call.
        Arguments:
            type (string): Must be one of these types:
              * `export_json`
              * `export_json_aggregated`
              * `export_csv`
              * `export_csv_aggregated`
              * `export_csv_flattened`
            filepath (string or IO or None): Location to save the results file. If not specified, will save to "project_{project_id}_results.{csv/json}
            poll_time (int): Number of seconds to poll for the report
        """
        return self.Report.save_report(
            self.id,
            type,
            filepath=filepath,
            poll_time=poll_time,
            api_key=api_key,
        )

    def download_json(self, poll_time=5 * 60, api_key: str = None):
        """
        Download and parse the results JSON for a project

        Arguments:
            poll_time (int): Number of seconds to poll for the report
        """
        return self.Report.download_json(self.id,
                                         poll_time=poll_time,
                                         api_key=api_key)
