from surge.errors import SurgeMissingIDError, SurgeTaskDataError
from surge.api_resource import PROJECTS_ENDPOINT, TASKS_ENDPOINT, APIResource
from surge.responses import TaskResponse


class Task(APIResource):
    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)

        if self.id is None or self.project_id is None:
            raise SurgeMissingIDError

        # If Task has responses, convert each into a TaskResponse object
        if hasattr(self, "responses"):
            task_responses = [
                TaskResponse(r["id"], r["data"], r["time_spent_in_secs"],
                             r["completed_at"], r["worker_id"])
                for r in self.responses
            ]
            self.responses = task_responses

    def __str__(self):
        return f"<surge.Task#{self.id}>"

    def __repr__(self):
        return f"<surge.Task#{self.id} {self.attrs_repr()}>"

    def attrs_repr(self):
        return self.print_attrs(forbid_list=["id"])

    def set_gold_standard(self,
                          gold_standard_answers=None,
                          is_gold_standard=True):
        '''Set gold standard answers for this task.

        Arguements:
        gold_standard_answers (List[string]): A list of the ground truth answers for this task, one for each question in the project.
            If you don't want to set an answer for one of the questions, you can leave it blank by passing an empty string.
        is_gold_standard (boolean): This indicates whether this task is a gold standard. You can toggle gold standards on or off by
            setting this as true or false.
        '''
        if self.id is None or self.project_id is None:
            raise SurgeMissingIDError
        endpoint = f"{TASKS_ENDPOINT}/{self.id}/gold-standards"
        data = {
            "is_gold_standard": is_gold_standard,
            'answers': gold_standard_answers
        }
        return self.post(endpoint, data)

    @classmethod
    def create(cls, project_id: str, **params):
        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}/{TASKS_ENDPOINT}"
        data = {"fields": params}
        response_json = cls.post(endpoint, data)
        return cls(**response_json)

    @classmethod
    def create_many(cls, project_id: str, tasks_data: list):
        '''
        Creates new Task objects for a given Project.

            Parameters:
                project_id (str): ID of the project to which the tasks are added
                tasks_data (list): list of dicts that map each task field to its value
                    e.g. [{"website": "surgehq.ai"}, {"website":"twitch.tv"}]

            Returns:
                tasks (list): list of Task objects
        '''
        if type(tasks_data) is not list or len(tasks_data) == 0:
            raise SurgeTaskDataError

        if not all(isinstance(t, dict) for t in tasks_data):
            raise SurgeTaskDataError

        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}/{TASKS_ENDPOINT}/create_tasks"
        data = {"tasks": tasks_data}
        response_json = cls.post(endpoint, data)
        tasks = [cls(**task_json) for task_json in response_json]
        return tasks

    @classmethod
    def list(cls, project_id: str, page: int = 1):
        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}/{TASKS_ENDPOINT}"
        params = {"page": page}
        response_json = cls.get(endpoint, params)
        tasks = [cls(**task_json) for task_json in response_json]
        return tasks

    @classmethod
    def retrieve(cls, task_id: str):
        endpoint = f"{TASKS_ENDPOINT}/{task_id}"
        response_json = cls.get(endpoint)
        return cls(**response_json)
