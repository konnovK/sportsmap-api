from __future__ import annotations

import logging
import os

from dataclasses import dataclass

from utils import setup_logger

logger = logging.getLogger(__name__)
setup_logger(logger)


@dataclass
class Settings:
    API_HOST: str | None
    API_PORT: int | None
    API_DB_URL: str
    API_DB_USE_SSL: bool

    @staticmethod
    def new() -> Settings:
        api_host = os.getenv('API_HOST')
        if api_host is None:
            logger.warning('API_HOST is none, use 0.0.0.0 by default')
            api_host = None

        api_port = os.getenv('API_PORT')
        if api_port is None:
            logger.warning('API_PORT is none, use 8080 by default')
            api_port = 8080

        api_db_url = os.getenv('API_DB_URL')
        if api_db_url is None:
            logger.warning('API_DB_URL is none')
            raise ValueError('CONFIG: ENVIRONMENT VARIABLE API_DB_URL is None')

        api_db_use_ssl = os.getenv('API_DB_USE_SSL')
        if api_db_use_ssl is None:
            logger.warning('API_DB_USE_SSL is none, use False by default')
            api_db_use_ssl = False
        else:
            api_db_use_ssl = True

        return Settings(
            API_HOST=api_host,
            API_PORT=api_port,
            API_DB_URL=api_db_url,
            API_DB_USE_SSL=api_db_use_ssl
        )
