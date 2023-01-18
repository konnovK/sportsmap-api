from aiohttp import web
from loguru import logger

from api_config import get_config
from api.app import create_app


def main():
    config = get_config()
    app = create_app(config)
    web.run_app(app, host=config.API_HOST, port=config.API_PORT, access_log=logger)


if __name__ == '__main__':
    main()
