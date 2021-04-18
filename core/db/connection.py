import os.path
import mariadb

import core

def connect(conf: core.DatabaseConfig, socket=False):
    """Connects to a MySQL instance.

    By default, the connection is attempted by authenticating with a Unix socket
    file and falls back to using a password if a socket file cannot be found.

    Returns a MySQL connection.
    """
    return _connect_with_socket(conf) if socket else _connect_with_password(conf)


def connect_for_testing(conf: core.DatabaseConfig, schema: str):
    """Connects to a MySQL instance intended to be used unit testing.

    For testing purposes, a schema file is read and temporary tables are
    created. These tables will be automatically cleaned up when the connection
    is closed.

    Returns a MySQL connection.
    """

    with open(schema, 'r') as f:
        data = f.read()
    
    tables = []
    # Split the schema into tables, and modify it to create temporary tables.
    for table in data.split(";"):
        t = table.lower().replace("create table if not exists",
            "create temporary table").strip()

        if len(t) > 0:
            tables.append(t)
    
    conn = connect(conf)
    for table in tables:
        with conn.cursor() as c:
            c.execute(table)

    return conn


def _connect_with_password(conf: core.DatabaseConfig):
    """Connects to a MySQL instance authenticating with a password."""

    conn = mariadb.connect(
        user=conf.user,
        password=conf.password,
        host=conf.host,
        port=conf.port,
        database=conf.database,
    )

    return conn


def _connect_with_socket(conf: core.DatabaseConfig):
    """Connects to a MySQL instance authenticating with a Unix socket file."""

    socket = _get_socket_file()
    if not os.path.isfile(socket):
        return _connect_with_password(conf)

    conn = mariadb.connect(
        user=conf.user,
        host=conf.host,
        database=conf.database,
        unix_socket=_get_socket_file(),
    )

    return conn


def _get_socket_file() -> str:
    """Returns a path to a unix socket file.
    
    The default path for Unix socket files for MySQL are not always common
    across different systems. We return the most common path if a file exists
    there, the second most common path otherwise.
    """

    socket = "/tmp/mysql.sock"
    if os.path.isfile(socket):
        return socket

    return "/var/run/mysqld/mysqld.sock"

