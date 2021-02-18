import pytest

import surge
from surge.api_resource import APIResource
from surge.errors import SurgeRequestError, SurgeMissingAPIKeyError


def test_raise_exception_if_missing_api_key():
    with pytest.raises(SurgeMissingAPIKeyError) as e_info:
        surge.api_key = None
        APIResource._base_request("get", surge.api_resource.PROJECTS_ENDPOINT)


def test_raise_exception_if_invalid_http_method():
    with pytest.raises(SurgeRequestError) as e_info:
        surge.api_key = "api-key"
        APIResource._base_request("test", surge.api_resource.PROJECTS_ENDPOINT)


def test_raise_exception_if_invalid_api_key():
    with pytest.raises(SurgeRequestError) as e_info:
        surge.api_key = "api-key"
        APIResource._base_request("get", surge.api_resource.PROJECTS_ENDPOINT)