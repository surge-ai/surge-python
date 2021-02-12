from surge.api_resource import APIResource

ENDPOINT = "projects"

class Projects(APIResource):
    def __init__(self):
        self.id = None

    @classmethod
    def create(cls,
            name,
            payment_per_response,
            instructions = None,
            questions = None,
            callback_url = None,
            fields_template = None,
            num_workers_per_task = 1):

        params = {
            "name": name,
            "payment_per_response": payment_per_response,
            "instructions": instructions,
            "questions": questions,
            "callback_url": callback_url,
            "field_template": fields_template,
            "num_workers_per_task": num_workers_per_task
        }
        return cls.post(ENDPOINT, params)

    @classmethod
    def list(cls, page_num=1):
        params = {"page_num": page_num}
        return cls.get(ENDPOINT, params)
    
    @classmethod
    def retrieve(cls, project_id):
        endpoint = f"{ENDPOINT}/{project_id}"
        return cls.get(endpoint)

    @classmethod
    def pause(cls, project_id):
        endpoint = f"{ENDPOINT}/{project_id}/pause"
        return cls.put(endpoint)
    
    @classmethod
    def resume(cls, project_id):
        endpoint = f"{ENDPOINT}/{project_id}/resume"
        return cls.put(endpoint)
    
    @classmethod
    def cancel(cls, project_id):
        endpoint = f"{ENDPOINT}/{project_id}/cancel"
        return cls.put(endpoint)
