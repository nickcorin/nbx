import unittest
import os.path

import core
from core import config

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "test_config.json")

TEST_DATABASE_CONFIG = config.DatabaseConfig(
    host="localhost",
    port=3306,
    user="nbx",
    password="crypto",
    database="nbx"
)

TEST_SERVER_CONFIG = config.ServerConfig(
    host="localhost",
    port=8080,
)

class TestConfig(unittest.TestCase):
    """Tests the config module."""

    def test_load_from_file(self):
        conf = config.load_from_file(TESTDATA_FILENAME)

        self.assertTrue(isinstance(conf, core.Config),
            "should be an instance of Config")
            
        self.assertTrue(isinstance(conf.server, core.ServerConfig),
            "should be an instance of ServerConfig")

        self.assertTrue(isinstance(conf.db, core.DatabaseConfig),
            "should be an instance of DatabaseConfig")

        self.assertEqual(TEST_DATABASE_CONFIG, conf.db)
        self.assertEqual(TEST_SERVER_CONFIG, conf.server)
