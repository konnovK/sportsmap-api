import logging

from aiohttp import web

from settings import Settings
from api.app import create_app
from utils import setup_logger

logger = logging.getLogger(__name__)
setup_logger(logger)


def main():
    settings = Settings.new()
    app = create_app(settings)
    web.run_app(app, host=settings.API_HOST, port=settings.API_PORT, access_log=logger, keepalive_timeout=5)


if __name__ == '__main__':
    main()
