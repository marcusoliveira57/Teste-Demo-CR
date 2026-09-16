import os
import unittest
from unittest.mock import patch

import requests

import api


class FetchTests(unittest.TestCase):
    @patch.dict(os.environ, {"API_KEY": "secret"}, clear=True)
    @patch("api.requests.get")
    def test_fetch_encodes_path_and_preserves_query_parameters(self, get):
        response = get.return_value
        response.json.return_value = {"ok": True}

        result = api.fetch(
            "users/José?role=admin&role=editor&empty=&key=untrusted"
        )

        get.assert_called_once_with(
            "https://api.exemplo.com/users/Jos%C3%A9",
            params=[
                ("role", "admin"),
                ("role", "editor"),
                ("empty", ""),
                ("key", "secret"),
            ],
            timeout=api.REQUEST_TIMEOUT,
        )
        response.raise_for_status.assert_called_once_with()
        self.assertEqual(result, {"ok": True})

    @patch.dict(os.environ, {}, clear=True)
    def test_fetch_requires_api_key(self):
        with self.assertRaisesRegex(RuntimeError, "API_KEY"):
            api.fetch("users")

    @patch.dict(os.environ, {"API_KEY": "secret"}, clear=True)
    def test_fetch_rejects_absolute_endpoint_and_fragment(self):
        invalid_endpoints = (
            "https://malicious.example/users",
            "//malicious.example/users",
            "/users",
            "users#details",
        )

        for endpoint in invalid_endpoints:
            with self.subTest(endpoint=endpoint):
                with self.assertRaises(ValueError):
                    api.fetch(endpoint)

    @patch.dict(os.environ, {"API_KEY": "secret"}, clear=True)
    @patch("api.requests.get")
    def test_fetch_propagates_http_error_without_reading_json(self, get):
        response = get.return_value
        response.raise_for_status.side_effect = requests.HTTPError("failure")

        with self.assertRaises(requests.HTTPError):
            api.fetch("users")

        response.json.assert_not_called()


if __name__ == "__main__":
    unittest.main()
