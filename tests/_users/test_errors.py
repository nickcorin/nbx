import unittest

from users import errors

class ErrorsTest(unittest.TestCase):
    """Tests the errors module."""

    def test_status_code(self):
        not_found = errors.status_code(errors.UserNotFound())
        self.assertEqual(not_found, 404, "Should return 404.")

        bad_request = errors.status_code(errors.InvalidEmail())
        self.assertEqual(bad_request, 400, "Should return 400.")

        unexpected_error = errors.status_code(ValueError())
        self.assertEqual(unexpected_error, 500, "Should return 500.")
