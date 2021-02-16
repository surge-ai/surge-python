import requests

import surge
from surge.errors import SurgeRequestError, SurgeMissingAPIKeyError

BASE_URL = "https://app.surgehq.ai/api"
PROJECTS_ENDPOINT = "projects"
TASKS_ENDPOINT = "tasks"


class APIResource(object):
    def __init__(self, id=None):
        self.id = id

    @classmethod
    def _base_request(cls, method, api_endpoint, params=None):
        if surge.api_key is None:
            raise SurgeMissingAPIKeyError

        try:
            url = f"{BASE_URL}/{api_endpoint}"

            # GET request
            if method == "get":
                response = requests.get(url,
                                        auth=(surge.api_key, ""),
                                        data=params)

            # POST request
            elif method == "post":
                response = requests.post(url,
                                         auth=(surge.api_key, ""),
                                         json=params)

            # PUT request
            elif method == "put":
                response = requests.put(url, auth=(surge.api_key, ""))

            # Raise exception if there is an http error
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as err:
            raise SurgeRequestError(err)

        except Exception:
            # Generic exception handling
            raise SurgeRequestError

    @classmethod
    def get(cls, api_endpoint, params=None):
        method = "get"
        return cls._base_request(method, api_endpoint, params=params)

    @classmethod
    def post(cls, api_endpoint, params=None):
        method = "post"
        return cls._base_request(method, api_endpoint, params=params)

    @classmethod
    def put(cls, api_endpoint, params=None):
        method = "put"
        return cls._base_request(method, api_endpoint, params=params)
