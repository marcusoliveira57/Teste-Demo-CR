import os
import unittest
from unittest.mock import Mock, patch

import api


class FetchTests(unittest.TestCase):
    @patch.dict(os.environ, {"API_KEY": "test-key"}, clear=True)
    @patch("api.requests.get")
    def test_fetch_builds_safe_request_and_checks_status(self, get):
        response = Mock()
        response.json.return_value = {"name": "Ada"}
        get.return_value = response

        result = api.fetch("users/Ada Lovelace?active=true")

        get.assert_called_once_with(
            "https://api.exemplo.com/users/Ada%20Lovelace",
            params={"active": "true", "key": "test-key"},
            timeout=api.REQUEST_TIMEOUT,
        )
        response.raise_for_status.assert_called_once_with()
        self.assertEqual(result, {"name": "Ada"})

    @patch.dict(os.environ, {}, clear=True)
    def test_fetch_requires_api_key(self):
        with self.assertRaises(RuntimeError):
            api.fetch("users")

    @patch.dict(os.environ, {"API_KEY": "test-key"}, clear=True)
    def test_fetch_rejects_absolute_endpoint(self):
        with self.assertRaises(ValueError):
            api.fetch("https://example.org/users")


if __name__ == "__main__":
    unittest.main()
