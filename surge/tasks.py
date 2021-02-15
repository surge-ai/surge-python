from surge.api_resource import PROJECTS_ENDPOINT, TASKS_ENDPOINT, APIResource

class Task(APIResource):
    def __init__(self):
        super().__init__()

    @classmethod
    def list(cls, project_id, page_num=1):
        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}/{TASKS_ENDPOINT}"
        params = {"page": page_num}
        return cls.get(endpoint, params)
    
    @classmethod
    def retrieve(cls, task_id):
        endpoint = f"{TASKS_ENDPOINT}/{task_id}"
        return cls.get(endpoint)
