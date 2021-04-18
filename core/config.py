from dataclasses import dataclass
from typing import NamedTuple

import json

@dataclass(frozen=True)
class ServerConfig:
    """Contains configuration options for an HTTP server."""

    host: str = "127.0.0.1"
    port: int = 8080


@dataclass(frozen=True)
class DatabaseConfig:
    """Contains database configuration options and connection details."""

    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "root"
    password: str = ""
    database: str = "nbx"


@dataclass(frozen=True)
class Config:
    """Wrapper class for application configuration options."""

    server: ServerConfig
    db: DatabaseConfig


def load_from_string(config_str: str):
    """Loads configuration options from a JSON string.
    
    Returns a Config object.
    """
    return Config(
        server = ServerConfig(**config_str["server"]),
        db = DatabaseConfig(**config_str["db"])
    )

def default():
    """Returns a Config object with default options.
    
    This is mostly used for unit testing when you need to connect to local
    databases.
    """
    return Config(server=ServerConfig(), db=DatabaseConfig())

def load_from_file(config_file: str):
    """Loads configuration options from a JSON file.
    
    Returns a Config object.
    """

    with open(config_file, 'r') as f:
        data = json.load(f)

    return load_from_string(data)

