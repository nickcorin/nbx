import unittest

from users.db import util

class TestUtil(unittest.TestCase):
    """Tests the util module."""

    def test_valid_email(self):
        # Valid emails.
        self.assertTrue(util.valid_email("test@example.com"))
        self.assertTrue(util.valid_email("test@example.com"))

        # Invalid emails.
        self.assertFalse(util.valid_email("test+alias@example.com"))
        self.assertFalse(util.valid_email("@example.com"))

        # Bogus inputs.
        self.assertFalse(util.valid_email(""))
        self.assertFalse(util.valid_email("@&*($"))