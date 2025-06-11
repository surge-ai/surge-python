import requests

import surge
from surge.errors import SurgeRequestError, SurgeMissingAPIKeyError

PROJECTS_ENDPOINT = "projects"
TASKS_ENDPOINT = "tasks"
REPORTS_ENDPOINT = "projects"
QUESTIONS_ENDPOINT = "items"
TEAMS_ENDPOINT = "teams"


class APIResource(object):

    def __init__(self, id=None):
        self.id = id

    def print_attrs(self, forbid_list: list = []):
        return " ".join([
            f'{k}="{v}"' for k, v in self.__dict__.items()
            if not k in forbid_list
        ])

    @classmethod
    def _base_request(cls,
                      method,
                      api_endpoint,
                      params=None,
                      files=None,
                      api_key=None):
        api_key_to_use = api_key or surge.api_key
        if api_key_to_use is None:
            raise SurgeMissingAPIKeyError

        if files is not None and method != "post":
            raise SurgeRequestError("Can only uploadfiles to a POST request")

        try:
            url = f"{surge.base_url}/{api_endpoint}"

            # GET request
            if method == "get":
                response = requests.get(url,
                                        auth=(api_key_to_use, ""),
                                        params=params)

            # POST request
            elif method == "post":
                if files is not None:
                    response = requests.post(url,
                                             auth=(api_key_to_use, ""),
                                             files=files,
                                             json=params)
                else:
                    response = requests.post(url,
                                             auth=(api_key_to_use, ""),
                                             json=params)

            # PUT request
            elif method == "put":
                if params is not None and len(params):
                    response = requests.put(url,
                                            auth=(api_key_to_use, ""),
                                            json=params)
                else:
                    response = requests.put(url, auth=(api_key_to_use, ""))

            elif method == "delete":
                response = requests.delete(url, auth=(api_key_to_use, ""))

            elif method == "patch":
                response = requests.patch(url,
                                          auth=(api_key_to_use, ""),
                                          json=params)

            else:
                raise SurgeRequestError("Invalid HTTP method.")

            # Raise exception if there is an http error
            response.raise_for_status()

            # If no errors, return response as json
            return response.json()

        except requests.exceptions.HTTPError as err:
            message = err.args[0]
            message = f"{message}. {err.response.text}"
            raise SurgeRequestError(message) from None

        except requests.exceptions.JSONDecodeError as err:
            message = err.args[0]
            raise SurgeRequestError(message) from None

        except Exception as err:
            # Generic exception handling
            raise SurgeRequestError

    @classmethod
    def get(cls, api_endpoint, params=None, api_key=None):
        method = "get"
        return cls._base_request(method,
                                 api_endpoint,
                                 params=params,
                                 api_key=api_key)

    @classmethod
    def post(cls, api_endpoint, params=None, api_key=None, files=None):
        method = "post"
        return cls._base_request(method,
                                 api_endpoint,
                                 params=params,
                                 api_key=api_key,
                                 files=files)

    @classmethod
    def put(cls, api_endpoint, params=None, api_key=None):
        method = "put"
        return cls._base_request(method,
                                 api_endpoint,
                                 params=params,
                                 api_key=api_key)

    @classmethod
    def patch(cls, api_endpoint, params=None, api_key=None):
        method = "patch"
        return cls._base_request(method,
                                 api_endpoint,
                                 params=params,
                                 api_key=api_key)

    @classmethod
    def delete_request(cls, api_endpoint, api_key=None):
        method = "delete"
        return cls._base_request(method, api_endpoint, api_key=api_key)
