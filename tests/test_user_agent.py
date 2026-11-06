from platform import python_version
from unittest.mock import Mock, patch

import pytest

import surge
from surge._version import __version__
from surge.api_resource import APIResource


@pytest.mark.parametrize("method,params,files", [
    ("get", None, None),
    ("post", None, None),
    ("post", None, {
        "file": ("task.txt", b"task")
    }),
    ("put", None, None),
    ("put", {
        "name": "test"
    }, None),
    ("patch", None, None),
    ("delete", None, None),
])
def test_prepared_request_identifies_sdk(method, params, files, monkeypatch):
    monkeypatch.setattr(surge, "default_headers", {})
    response = Mock()
    response.json.return_value = {}
    with patch("requests.sessions.Session.send",
               return_value=response) as send:
        APIResource._base_request(method,
                                  "projects",
                                  params=params,
                                  files=files,
                                  api_key="test-key")
    request = send.call_args.args[0]
    assert request.headers[
        "User-Agent"] == f"surge-python/{__version__} Python/{python_version()}"


@pytest.mark.parametrize("header", ["User-Agent", "user-agent", "USER-AGENT"])
def test_custom_user_agent_is_preserved(header, monkeypatch):
    custom_headers = {header: "custom-client/1.0", "X-Actor-Type": "agent"}
    monkeypatch.setattr(surge, "default_headers", custom_headers)
    response = Mock()
    response.json.return_value = {}
    with patch("requests.sessions.Session.send",
               return_value=response) as send:
        APIResource._base_request("get", "projects", api_key="test-key")
    request = send.call_args.args[0]
    assert request.headers["User-Agent"] == "custom-client/1.0"
    assert request.headers["X-Actor-Type"] == "agent"
    assert surge.default_headers == custom_headers
