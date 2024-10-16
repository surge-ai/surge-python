from io import StringIO
from unittest import mock
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


def test_passed_in_api_key():
    with mock.patch.object(requests, "get") as mock_request:
        mock_request.return_value = mock.MagicMock()
        APIResource._base_request(
            "get", surge.api_resource.PROJECTS_ENDPOINT, api_key="passed_api_key"
        )
        mock_request.assert_called_once_with(
            "https://app.surgehq.ai/api/projects",
            auth=("passed_api_key", ""),
            params=None,
        )


def test_passed_in_file():
    with mock.patch.object(requests, "post") as mock_request:
        files = {"file": StringIO()}
        mock_request.return_value = mock.MagicMock()
        APIResource._base_request(
            "post",
            surge.api_resource.PROJECTS_ENDPOINT,
            files=files,
            api_key="passed_api_key",
        )
        mock_request.assert_called_once_with(
            "https://app.surgehq.ai/api/projects",
            auth=("passed_api_key", ""),
            files=files,
            json=None,
        )


def test_get_passed_in_file():
    with pytest.raises(SurgeRequestError) as e_info:
        files = {"file": StringIO()}
        APIResource._base_request(
            "get",
            surge.api_resource.PROJECTS_ENDPOINT,
            files=files,
            api_key="passed_api_key",
        )


def test_print_attrs():
    a1 = APIResource(id="ABC1234").print_attrs()
    assert a1 == 'id="ABC1234"'
