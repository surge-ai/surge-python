import pytest
import requests

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


def test_passed_in_api_key(mocker):
    mock_request = mocker.patch.object(requests, 'get')
    APIResource._base_request("get", surge.api_resource.PROJECTS_ENDPOINT, api_key="passed_api_key")
    mock_request.assert_called_once_with("https://app.surgehq.ai/api/projects", auth=("passed_api_key", ""), params=None)

def test_print_attrs():
    a1 = APIResource(id="ABC1234").print_attrs()
    assert a1 == 'id="ABC1234"'
