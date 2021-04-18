from dataclasses import dataclass

import core

from core import db
from users.db import users


class State:
    """Contains client dependencies of the users service."""

    def __init__(self, conf: core.Config):
        self._db = db.connect(conf.db)
        self._users_repo = users.Repository(self._db)


    @property
    def db(self):
        """Returns a connection to the main database."""
        return self._db
    

    @property
    def users_repo(self):
        """Returns an instance to a UsersRepositiry."""
        return self._users_repo

