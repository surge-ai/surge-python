from surge.api_resource import PROJECTS_ENDPOINT, APIResource
from surge.questions import Question
from surge.errors import SurgeProjectQuestionError

class Projects(APIResource):
    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls,
            name,
            payment_per_response,
            instructions = None,
            questions = None,
            callback_url = None,
            fields_template = None,
            num_workers_per_task = 1):

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
        return cls.post(PROJECTS_ENDPOINT, params)

    @classmethod
    def list(cls, page_num=1):
        params = {"page_num": page_num}
        return cls.get(PROJECTS_ENDPOINT, params)
    
    @classmethod
    def retrieve(cls, project_id):
        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}"
        return cls.get(endpoint)

    @classmethod
    def pause(cls, project_id):
        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}/pause"
        return cls.put(endpoint)
    
    @classmethod
    def resume(cls, project_id):
        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}/resume"
        return cls.put(endpoint)
    
    @classmethod
    def cancel(cls, project_id):
        endpoint = f"{PROJECTS_ENDPOINT}/{project_id}/cancel"
        return cls.put(endpoint)
