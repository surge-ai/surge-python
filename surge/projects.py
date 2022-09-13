import dateutil.parser

from surge.errors import SurgeMissingIDError, SurgeProjectQuestionError, SurgeMissingAttributeError
from surge.api_resource import PROJECTS_ENDPOINT, APIResource
from surge.questions import Question, FreeResponseQuestion, MultipleChoiceQuestion, CheckboxQuestion, TextTaggingQuestion, TreeSelectionQuestion, FileUpload, RankingQuestion, ChatBot, TextArea
from surge.tasks import Task
from surge import utils


class Project(APIResource):
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
        return f"<surge.Project#{self.id} name=\"{self.name}\">"

    def __repr__(self):
        return f"<surge.Project#{self.id} name=\"{self.name}\" {self.attrs_repr()}>"

    def attrs_repr(self):
        return self.print_attrs(forbid_list=["name", "id"])

    def _convert_questions_to_objects(self, questions_data):
        questions = []
        for q in questions_data:
            if q["type"] == "free_response":
                questions.append(
                    FreeResponseQuestion(
                        q["text"],
                        required=q["required"],
                        preexisting_annotations=q["preexisting_annotations"]))
            elif q["type"] == "multiple_choice":
                questions.append(
                    MultipleChoiceQuestion(
                        q["text"],
                        options=q["options"],
                        required=q["required"],
                        preexisting_annotations=q["preexisting_annotations"],
                        require_tiebreaker=q["require_tie_breaker"]))

            elif q["type"] == "checkbox":
                questions.append(
                    CheckboxQuestion(q["text"],
                                     options=q["options"],
                                     required=q["required"],
                                     preexisting_annotations=q["preexisting_annotations"],
                                     require_tiebreaker=q["require_tie_breaker"]))
            elif q["type"] == "text_tagging":
                questions.append(
                    TextTaggingQuestion(
                        q["text"],
                        required=q["required"],
                        options=q["options"],
                        preexisting_annotations=q["preexisting_annotations"],
                        token_granularity=q["ner_token_granularity"],
                        allow_relationship_tags=q["ner_allow_relationship_tags"],
                        allow_overlapping_tags=q["ner_allow_overlapping_tags"],
                        require_tiebreaker=q["require_tie_breaker"]))

            elif q["type"] == "tree_selection":
                questions.append(
                    TreeSelectionQuestion(
                        q["text"],
                        options=q["options"],
                        required=q["required"],
                        preexisting_annotations=q["preexisting_annotations"],
                        require_tiebreaker=q["require_tie_breaker"]))
            elif q["type"] == "ranking":
                questions.append(
                    RankingQuestion(
                        q["text"],
                        options=q["options"],
                        required=q["required"],
                        preexisting_annotations=q["preexisting_annotations"],
                        allow_ranking_ties=q["allow_ranking_ties"]))
            elif q["type"] == "file_upload":
                questions.append(
                    FileUpload(q["text"],
                               required=q["required"]))
            elif q["type"] == "text":
                questions.append(
                    TextTaggingQuestion(q["text"]))
        return questions

    @staticmethod
    def _validate_questions(questions):
        # Convert list of question objects into dicts in valid json format
        # If this isn't a list of Question objects, throw an exception
        if not all(isinstance(q, Question) for q in questions):
            raise SurgeProjectQuestionError

    @classmethod
    def create(cls,
               name: str,
               payment_per_response: float = None,
               private_workforce: bool = False,
               instructions: str = None,
               questions: list = [],
               qualifications_required: list = [],
               teams_required: list = [],
               callback_url: str = None,
               fields_template: str = None,
               num_workers_per_task: int = 1,
               tags=[]):
        '''
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
            callback_url (str, optional): url that receives a POST request with the project's data.
            fields_template (str, optional): A template describing how fields are shown to workers working on the task.
                For example, if fields_template is "{{company_name}}", then workers will be shown a link to the company.
            num_workers_per_task (int, optional): How many workers work on each task (i.e., how many responses per task).
            tags (list, optional): An array of strings to tag the project with. Worker won't see these tags.

        Returns:
            project: new Project object
        '''

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
            "callback_url": callback_url,
            "fields_template": fields_template,
            "num_workers_per_task": num_workers_per_task,
            "tags": tags
        }
        if payment_per_response is not None:
            params["payment_per_response"] = payment_per_response
        response_json = cls.post(PROJECTS_ENDPOINT, params)
        return cls(**response_json)

    @classmethod
    def list(cls, page: int = 1):
        '''
        Lists all projects you have created.
        Projects are returned in descending order of created_at.
        Each page contains a maximum of 100 projects.

        Arguments:
            page (int, optional): Page number to retrieve. Pages start at 1 (default value).

        Returns:
            projects (list): list of Project objects.
        '''
        params = {"page": page}
        response_json = cls.get(PROJECTS_ENDPOINT, params)
        projects = [cls(**project_json) for project_json in response_json]
        return projects

    @classmethod
    def list_shared(cls, page: int = 1):
        '''
        Lists all projects created by anyone in your organization.
        Projects are returned in descending order of created_at.
        Each page contains a maximum of 100 projects.

        Arguments:
            page (int, optional): Page number to retrieve. Pages start at 1 (default value).

        Returns:
            projects (list): list of Project objects.
        '''
        params = {"page": page}
        endpoint = f"{PROJECTS_ENDPOINT}/shared"
        response_json = cls.get(endpoint, params)
        projects = [cls(**project_json) for project_json in response_json]
        return projects

    @classmethod
    def retrieve(cls, project_id: str):
        '''
        Retrieves a specific project you have created.

        Arguments:
            project_id (str): ID of project.

        Returns:
            project: Project object
        '''
        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}"
        response_json = cls.get(endpoint)
        return cls(**response_json)

    def launch(self):
        '''
        Launches a project.
        If work is being completed by the Surge workforce, you will be charged when the project launches
        and your accounts neeeds to have sufficient funds before launching.

        Returns:
            project: new Project object with updated status
        '''
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/launch"
        return self.put(endpoint)

    def pause(self):
        '''
        Pauses a project.
        Tasks added to the project will not be worked on until you resume the project.

        Returns:
            project: new Project object with updated status
        '''
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/pause"
        return self.put(endpoint)

    def resume(self):
        '''
        Resumes a paused project.

        Returns:
            project: new Project object with updated status
        '''
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/resume"
        return self.put(endpoint)

    def cancel(self):
        '''
        Cancels a project.

        Returns:
            project: new Project object with updated status
        '''
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/cancel"
        return self.put(endpoint)

    def list_tasks(self, page: int = 1, per_page: int = 100):
        '''
        Lists all tasks belonging to this project.
        Tasks are returned in ascending order of created_at.
        Each page contains a maximum of 25 tasks.

        Arguments:
            page (int, optional): Page number to retrieve. Pages start at 1 (default value).

        Returns:
            tasks (list): list of Task objects.
        '''
        return Task.list(self.id, page=page, per_page=per_page)

    def create_tasks(self, tasks_data: list, launch=False):
        '''
        Creates new Task objects for this project.

        Arguments:
            tasks_data (list): list of dicts that map each task field to its value
                e.g. [{"website": "surgehq.ai"}, {"website":"twitch.tv"}]

        Returns:
            tasks (list): list of Task objects
        '''
        return Task.create_many(self.id, tasks_data, launch)

    def create_tasks_from_csv(self, file_path: str):
        '''
        Creates new Task objects for this project from a local CSV file.
        The header of the CSV file must specify the fields that are used in your Tasks.

        Arguments:
            file_path (str): path to CSV file.

        Returns:
            tasks (list): list of Task objects
        '''
        tasks_data = utils.load_tasks_data_from_csv(file_path)
        return self.create_tasks(tasks_data)

    def update(self,
               name: str = None,
               payment_per_response: float = None,
               instructions: str = None,
               callback_url: str = None,
               fields_template: str = None,
               num_workers_per_task: int = 0):
        '''
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
        '''

        params = {}

        Project._validate_questions(questions)
        questions_json = [q.to_dict() for q in questions]

        if name is not None and len(name) > 0:
            params["name"] = name
        if payment_per_response is not None:
            params["payment_per_response"] = payment_per_response
        if instructions is not None and len(instructions) > 0:
            params["instructions"] = instructions
        if callback_url is not None and len(callback_url) > 0:
            params["callback_url"] = callback_url
        if num_workers_per_task > 0:
            params["num_workers_per_task"] = num_workers_per_task

        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}"
        response_json = self.put(endpoint, params)
        return Project(**response_json)
