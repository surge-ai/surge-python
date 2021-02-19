from surge.errors import SurgeMissingIDError, SurgeProjectQuestionError
from surge.api_resource import PROJECTS_ENDPOINT, APIResource
from surge.questions import Question
from surge.tasks import Task
from surge import utils


class Project(APIResource):
    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)

        if self.id is None:
            raise SurgeMissingIDError

    def __str__(self):
        return f"<surge.Project#{self.id} name=\"{self.name}\">"

    def __repr__(self):
        return f"<surge.Project#{self.id} name=\"{self.name}\" {self.attrs_repr()}>"

    def attrs_repr(self):
        return self.print_attrs(forbid_list=["name", "id"])

    @classmethod
    def create(cls,
               name: str,
               payment_per_response: float = None,
               private_workforce: bool = False,
               instructions: str = None,
               questions: list = [],
               callback_url: str = None,
               fields_template: str = None,
               num_workers_per_task: int = 1):

        # Convert list of question objects into dicts in valid json format
        # If this isn't a list of Question objects, throw an exception
        if not all(isinstance(q, Question) for q in questions):
            raise SurgeProjectQuestionError

        questions_json = [q.to_dict() for q in questions]

        params = {
            "name": name,
            "private_workforce": private_workforce,
            "instructions": instructions,
            "questions": questions_json,
            "callback_url": callback_url,
            "field_template": fields_template,
            "num_workers_per_task": num_workers_per_task
        }
        if payment_per_response is not None:
            params["payment_per_response"] = payment_per_response
        response_json = cls.post(PROJECTS_ENDPOINT, params)
        return cls(**response_json)

    @classmethod
    def list(cls, page: int = 1):
        params = {"page": page}
        response_json = cls.get(PROJECTS_ENDPOINT, params)
        projects = [cls(**project_json) for project_json in response_json]
        return projects

    @classmethod
    def retrieve(cls, project_id: str):
        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}"
        response_json = cls.get(endpoint)
        return cls(**response_json)

    def pause(self):
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/pause"
        return self.put(endpoint)

    def resume(self):
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/resume"
        return self.put(endpoint)

    def cancel(self):
        endpoint = f"{PROJECTS_ENDPOINT}/{self.id}/cancel"
        return self.put(endpoint)

    def list_tasks(self, page: int = 1):
        return Task.list(self.id, page=page)

    def create_tasks(self, tasks_data: list):
        '''
        Creates new Task objects for the current Project.

            Parameters:
                tasks_data (list): list of dicts that map each task field to its value
                    e.g. [{"website": "surgehq.ai"}, {"website":"twitch.tv"}]

            Returns:
                tasks (list): list of Task objects
        '''
        return Task.create_many(self.id, tasks_data)

    def create_tasks_from_csv(self, file_path: str):
        tasks_data = utils.load_tasks_data_from_csv(file_path)
        return self.create_tasks(tasks_data)
