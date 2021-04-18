from dataclasses import dataclass
from typing import List

import mariadb
import uuid

from users import errors
from users import types
from users.db import util

class Repository:
    """ Manages reads and writes to the `users` table."""

    _cols = "uuid, name, email, created_at, updated_at"

    def __init__(self, conn):
        self._conn = conn


    def create(self, name: str, email: str) -> str:
        """Inserts a new record into the `users` table.

        InvalidEmail is returned if the provided email is not in the correct 
        format.
        
        Returns the unique UUID generated for the user.
        """
        
        # Validate the email.
        if not util.valid_email(email):
            raise errors.InvalidEmail
        
        # Check if the email exists in the db yet.
        try:
            _ = self.lookup_by_email(email)
            raise errors.DuplicateEmail
        except errors.UserNotFound:
            # This email does not exist yet.
            pass

        # Generate the unique uuid for the new user.
        uid = uuid.uuid4().__str__()

        with self._conn.cursor() as c:
            c.execute("insert into users set uuid=?, name=?, email=?, "+
            "created_at=now(), updated_at=now()", (uid, name, email,))

        return uid


    def lookup(self, uid: str) -> types.User:
        """Queries the `users` table by uuid.

        Returns a User object on success, and UserNotFound on a query miss.
        """

        with self._conn.cursor() as c:
            c.execute(f"select {self._cols} from users where uuid=?", (uid,))
            return self._scan_row(c)
        
    def lookup_by_email(self, email: str) -> types.User:
        """Queries the `users` table by email.
        
        Returns a User object on success, and UserNotFound on a query miss.
        """

        with self._conn.cursor() as c:
            c.execute(f"select {self._cols} from users where email=?", (email,))
            return self._scan_row(c)


    def list_all(self) -> List[types.User]:
        """Lists all the records in the `users` table.
        
        Returns a list of User objects.
        """

        users = []
        with self._conn.cursor() as c:
            c.execute(f"select {self._cols} from users")
            users = self._scan_many(c)

        return users


    def update_details(self, uid: str, name: str, email: str):
        """Updates a user's name and / or email address."""

        # We lookup the user to make sure that the record exists, before running
        # the update.
        _ = self.lookup(uid)

        with self._conn.cursor() as c:
            c.execute("update users set name=?, email=?, updated_at=now() " +
                "where uuid=?", (name, email, uid,))


    def delete(self, uid: str):
        """Deletes a user from the `users` table.

        A hard delete is performed, so please use with caution.
        """

        try:
            with self._conn.cursor() as c:
                c.execute("delete from users where uuid=?", (uid,))
        except Exception as e:
            print(e)
    

    def _scan_row(self, cursor) -> types.User:
        """Unpacks the result tuple into a User object.
        
        Returns a User object, or UserNotFound for an empty result.
        """

        row = cursor.fetchone()
        if row is None:
            raise errors.UserNotFound
        
        (uid, name, email, created_at, updated_at,) = row
        return types.User(uid, name, email, created_at, updated_at)
    

    def _scan_many(self, cursor) -> List[types.User]:
        """Unpacks multiple rows into a List of User objects.
        
        Returns a User object, or UserNotFound for an empty result.
        """

        users = []
        for row in cursor.fetchall():
            (uid, name, email, created_at, updated_at,) = row
            users.append(types.User(uid, name, email, created_at, updated_at))

        return users