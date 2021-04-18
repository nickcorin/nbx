import unittest

from core import config
from users import (db, errors, types)
from users.db import users


class TestUsers(unittest.TestCase):
    """Tests the users module."""

    def setUp(self):
        conf = config.default()
        self._conn = db.connect_for_testing(conf.db)
        self._users_repo = users.Repository(self._conn)
    

    def tearDown(self):
        self._conn.close()


    def test_create(self):
        uid = self._users_repo.create("Satoshi Nakamoto", "satoshi@bitcoin.com")
        self.assertIsNotNone(uid)

        self.assertRaises(errors.InvalidEmail, self._users_repo.create,
            "Satoshi Nakamoto", "")


    def test_lookup(self):
        self.assertRaises(errors.UserNotFound, self._users_repo.lookup, "123")

        uid = self._users_repo.create("Satoshi Nakamoto", "satoshi@bitcoin.com")
        self.assertIsNotNone(uid)

        u = self._users_repo.lookup(uid)
        self.assertIsNotNone(u)

        self.assertEqual(u.uid, uid)
        self.assertEqual(u.name, "Satoshi Nakamoto")
        self.assertEqual(u.email, "satoshi@bitcoin.com")


    def test_list_all(self):
        uid = self._users_repo.create("Satoshi Nakamoto", "satoshi@bitcoin.com")
        self.assertIsNotNone(uid)

        uid = self._users_repo.create("Vitalik Buterin", "vitalik@ethereum.org")
        self.assertIsNotNone(uid)

        users = self._users_repo.list_all()
        self.assertEqual(2, len(users))

    
    def test_update_details(self):
        uid = self._users_repo.create("Satoshi Nakamoto", "satoshi@bitcoin.com")
        self.assertIsNotNone(uid)

        self._users_repo.update_details(uid, "Vitalik Buterin",
            "vitalik@ethereum.org")

        u = self._users_repo.lookup(uid)
        self.assertIsNotNone(u)
        self.assertEqual(u.name, "Vitalik Buterin")
        self.assertEqual(u.email, "vitalik@ethereum.org")
    
    
    def test_delete(self):
        uid = self._users_repo.create("Satoshi Nakamoto", "satoshi@bitcoin.com")
        self.assertIsNotNone(uid)

        self._users_repo.delete(uid)
        self.assertRaises(errors.UserNotFound, self._users_repo.lookup, uid)
