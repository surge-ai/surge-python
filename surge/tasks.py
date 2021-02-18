from surge.errors import SurgeMissingIDError
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
        return f"SurgeTask_{self.id}"

    @classmethod
    def create(cls, project_id: str, **params):
        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}/{TASKS_ENDPOINT}"
        data = {"fields": params}
        response_json = cls.post(endpoint, data)
        return cls(**response_json)

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
