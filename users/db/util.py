import re

def valid_email(email: str) -> bool:
    """Validates an email format using regex."""

    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    return True if re.search(regex, email) is not None else False