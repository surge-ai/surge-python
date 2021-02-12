import requests

import surge

BASE_URL = "https://app.surgehq.ai/api"
PROJECTS_ENDPOINT = "projects"
TASKS_ENDPOINT = "tasks"

class APIResource(object):
    def __init__(self):
        self.api_key = surge.api_key

    @classmethod
    def get(cls, api_endpoint, params = None):
        url = f"{BASE_URL}/{api_endpoint}"

        response_json = requests.get(
            url,
            auth = (surge.api_key, ""),
            data = params
        ).json()

        return response_json

    @classmethod
    def post(cls, api_endpoint, params = None):
        url = f"{BASE_URL}/{api_endpoint}"

        response_json = requests.post(
            url,
            auth = (surge.api_key, ""),
            json = params
        ).json()

        return response_json
    
    @classmethod
    def put(cls, api_endpoint):
        url = f"{BASE_URL}/{api_endpoint}"

        response_json = requests.put(
            url,
            auth = (surge.api_key, "")
        ).json()

        return response_json
