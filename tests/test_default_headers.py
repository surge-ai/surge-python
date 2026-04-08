import unittest
from unittest.mock import patch, MagicMock

import surge


class TestDefaultHeaders(unittest.TestCase):

    def setUp(self):
        surge.api_key = "test-key"
        surge.default_headers = {}

    def tearDown(self):
        surge.default_headers = {}

    @patch("requests.get")
    def test_no_default_headers(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from surge.api_resource import APIResource
        APIResource._base_request("get", "projects/123")

        call_kwargs = mock_get.call_args
        assert "headers" not in call_kwargs.kwargs

    @patch("requests.get")
    def test_actor_type_header_injected(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        surge.default_headers = {"X-Actor-Type": "agent"}

        from surge.api_resource import APIResource
        APIResource._base_request("get", "projects/123")

        call_kwargs = mock_get.call_args
        assert call_kwargs.kwargs["headers"] == {"X-Actor-Type": "agent"}

    @patch("requests.get")
    def test_default_headers_are_copied(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        surge.default_headers = {"X-Actor-Type": "agent"}

        from surge.api_resource import APIResource
        APIResource._base_request("get", "projects/123")

        # Mutate after the call — should not affect what was sent
        surge.default_headers["X-Extra"] = "oops"

        sent_headers = mock_get.call_args.kwargs["headers"]
        assert sent_headers == {"X-Actor-Type": "agent"}


if __name__ == "__main__":
    unittest.main()
