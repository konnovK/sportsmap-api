import logging

from aiohttp import web

from api_config import Config
from api.app import create_app
from utils import setup_logger

logger = logging.getLogger(__name__)
setup_logger(logger)


def main():
    config = Config.new()
    app = create_app(config)
    web.run_app(app, host=config.API_HOST, port=config.API_PORT, access_log=logger, keepalive_timeout=5)


if __name__ == '__main__':
    main()
