import os.path

import core

from core import db

# This is the path to the SQL schema for the users service.
SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")

def connect_for_testing(conf: core.DatabaseConfig):
    return db.connect_for_testing(conf, os.path.abspath(SCHEMA))