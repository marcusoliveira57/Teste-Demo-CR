import unittest
from unittest.mock import Mock, patch

import users


class GetUserTests(unittest.TestCase):
    @patch("users.connect_db")
    def test_get_user_uses_parameterized_query_and_closes_connection(self, connect_db):
        db = Mock()
        db.execute.return_value.fetchall.return_value = [(1, "Ada")]
        connect_db.return_value = db

        result = users.get_user("1 OR 1=1")

        db.execute.assert_called_once_with(
            "SELECT * FROM users WHERE id = ?",
            ("1 OR 1=1",),
        )
        db.close.assert_called_once_with()
        self.assertEqual(result, [(1, "Ada")])

    @patch("users.connect_db")
    def test_get_user_closes_connection_when_query_fails(self, connect_db):
        db = Mock()
        db.execute.side_effect = RuntimeError("query failed")
        connect_db.return_value = db

        with self.assertRaises(RuntimeError):
            users.get_user(1)

        db.close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
