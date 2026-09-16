import unittest
from unittest.mock import patch

import users


class GetUserTests(unittest.TestCase):
    @patch("users.connect_db")
    def test_get_user_uses_parameterized_query_and_closes_connection(self, connect):
        db = connect.return_value
        cursor = db.execute.return_value
        cursor.fetchall.return_value = [(7, "Ada")]

        result = users.get_user("7 OR 1=1")

        db.execute.assert_called_once_with(
            "SELECT * FROM users WHERE id = ?",
            ("7 OR 1=1",),
        )
        self.assertEqual(result, [(7, "Ada")])
        db.close.assert_called_once_with()

    @patch("users.connect_db")
    def test_get_user_closes_connection_after_query_failure(self, connect):
        db = connect.return_value
        db.execute.side_effect = RuntimeError("query failed")

        with self.assertRaisesRegex(RuntimeError, "query failed"):
            users.get_user(7)

        db.close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
