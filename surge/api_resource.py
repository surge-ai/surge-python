import requests

import surge
from surge.errors import SurgeRequestError

BASE_URL = "https://app.surgehq.ai/api"
PROJECTS_ENDPOINT = "projects"
TASKS_ENDPOINT = "tasks"

class APIResource(object):
    def __init__(self, id=None):
        self.id = id

    @classmethod
    def get(cls, api_endpoint, params = None):
        try:
            url = f"{BASE_URL}/{api_endpoint}"

            response = requests.get(
                url,
                auth = (surge.api_key, ""),
                data = params
            )

            # Raise exception if there is an http error
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as err:
            raise SurgeRequestError(err)

        except Exception:
            # Generic exception handling
            raise SurgeRequestError

    @classmethod
    def post(cls, api_endpoint, params = None):
        try:
            url = f"{BASE_URL}/{api_endpoint}"

            response = requests.post(
                url,
                auth = (surge.api_key, ""),
                json = params
            )

            # Raise exception if there is an http error
            response.raise_for_status()

            return response.json()
        
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        except Exception:
            # Generic exception handling
            raise SurgeRequestError
    
    @classmethod
    def put(cls, api_endpoint):
        try:
            url = f"{BASE_URL}/{api_endpoint}"

            response = requests.put(
                url,
                auth = (surge.api_key, "")
            )

            # Raise exception if there is an http error
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        except Exception:
            # Generic exception handling
            raise SurgeRequestError
