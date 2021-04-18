import datetime
import json

from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    """Represents a record in the users table."""

    uid: str
    name: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class ResponseEncoder(json.JSONEncoder):
    """Utility class to encode our types to JSON."""
    
    def default(self, obj):
        if isinstance(obj, User):
            return obj.__dict__

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)
