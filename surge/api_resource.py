import requests

import surge
from surge.errors import SurgeAuthError

BASE_URL = "https://app.surgehq.ai/api"
PROJECTS_ENDPOINT = "projects"
TASKS_ENDPOINT = "tasks"

class APIResource(object):
    def __init__(self, id=None):
        self.id = id

    @classmethod
    def get(cls, api_endpoint, params = None):
        url = f"{BASE_URL}/{api_endpoint}"

        response = requests.get(
            url,
            auth = (surge.api_key, ""),
            data = params
        )

        if response.status_code == 401:
            raise SurgeAuthError

        return response.json()

    @classmethod
    def post(cls, api_endpoint, params = None):
        url = f"{BASE_URL}/{api_endpoint}"

        response = requests.post(
            url,
            auth = (surge.api_key, ""),
            json = params
        )

        if response.status_code == 401:
            raise SurgeAuthError

        return response.json()
    
    @classmethod
    def put(cls, api_endpoint):
        url = f"{BASE_URL}/{api_endpoint}"

        response = requests.put(
            url,
            auth = (surge.api_key, "")
        )

        if response.status_code == 401:
            raise SurgeAuthError

        return response.json()
