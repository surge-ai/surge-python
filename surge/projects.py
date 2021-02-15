from surge.api_resource import PROJECTS_ENDPOINT, APIResource
from surge.questions import Question
from surge.errors import SurgeProjectQuestionError


class Project(APIResource):
    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)
        assert self.id is not None

    def __str__(self):
        return f"SurgeProject_{self.id}"

    @classmethod
    def create(cls,
               name,
               payment_per_response,
               instructions=None,
               questions=None,
               callback_url=None,
               fields_template=None,
               num_workers_per_task=1):

        # Convert list of question objects into dicts in valid json format
        # If this isn't a list of Question objects, throw an exception
        if not all(isinstance(q, Question) for q in questions):
            raise SurgeProjectQuestionError

        questions_json = [q.to_dict() for q in questions]

        params = {
            "name": name,
            "payment_per_response": payment_per_response,
            "instructions": instructions,
            "questions": questions_json,
            "callback_url": callback_url,
            "field_template": fields_template,
            "num_workers_per_task": num_workers_per_task
        }
        response_json = cls.post(PROJECTS_ENDPOINT, params)
        return cls(**response_json)

    @classmethod
    def list(cls, page_num=1):
        params = {"page_num": page_num}
        response_json = cls.get(PROJECTS_ENDPOINT, params)
        projects = [cls(**project_json) for project_json in response_json]
        return projects

    @classmethod
    def retrieve(cls, project_id):
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
