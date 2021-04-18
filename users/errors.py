class UsersError(Exception):
    """Base class for exceptions in this module."""
    pass


class DuplicateEmail(UsersError):
    """Returned when registering a user with an email that already exists."""

    def __init__(self):
        self.status_code = 400

    def __str__(self):
        return "email already exists"


class UserNotFound(UsersError):
    """Returned when querying for a user that does not exist."""

    def __init__(self):
        self.status_code = 404

    def __str__(self):
        return "user does not exist"


class InvalidEmail(UsersError):
    """Returned when providing an invalid email address."""

    def __init__(self):
        self.status_code = 400

    def __str__(self):
        return "invalid email provided"


def status_code(e: UsersError) -> int:
    """ Returns an HTTP status code for some Error."""

    if isinstance(e, UsersError):
        return e.status_code

    return 500