from surge.api_resource import PROJECTS_ENDPOINT, TASKS_ENDPOINT, APIResource


class Task(APIResource):
    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)
        assert self.id is not None
        assert self.project_id is not None

    def __str__(self):
        return f"SurgeTask_{self.id}"

    @classmethod
    def list(cls, project_id, page_num=1):
        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}/{TASKS_ENDPOINT}"
        params = {"page": page_num}
        response_json = cls.get(endpoint, params)
        tasks = [cls(**task_json) for task_json in response_json]
        return tasks

    @classmethod
    def retrieve(cls, task_id):
        endpoint = f"{TASKS_ENDPOINT}/{task_id}"
        response_json = cls.get(endpoint)
        return cls(**response_json)
