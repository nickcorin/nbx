from aiohttp import web
import logging
import os

from users import (server, state)
from core import config

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
LOGGER = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    LOGGER.info('### Starting user service ###')

    conf = config.load_from_file(CONFIG_PATH)
    state = state.State(conf)

    app = server.init(state)

    web.run_app(
        app=app,
        port=conf.server.port,
    )