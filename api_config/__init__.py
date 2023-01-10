import os

from loguru import logger
from dataclasses import dataclass


@dataclass
class Config:
    API_PORT: int | None
    API_DB_USER: str | None
    API_DB_PASSWORD: str | None
    API_DB_HOST: str | None
    API_DB_PORT: str | None
    API_DB_NAME: str | None
    API_DB_USE_SSL: bool
    API_DEBUG_MODE: bool


def get_config() -> Config:
    API_PORT = os.getenv('API_PORT')
    if not API_PORT:
        logger.warning('API_PORT is none, use 8080 by default')
        API_PORT = 8080
    try:
        API_PORT = int(API_PORT)
    except ValueError:
        logger.warning('API_PORT is not int, use 8080 by default')
        API_PORT = 8080

    API_DB_USER = os.getenv('API_DB_USER')
    if not API_DB_USER:
        logger.warning('API_DB_USER is none')

    API_DB_PASSWORD = os.getenv('API_DB_PASSWORD')
    if not API_DB_PASSWORD:
        logger.warning('API_DB_PASSWORD is none')

    API_DB_HOST = os.getenv('API_DB_HOST')
    if not API_DB_HOST:
        logger.warning('API_DB_HOST is none')

    API_DB_PORT = os.getenv('API_DB_PORT')
    if not API_DB_PORT:
        logger.warning('API_DB_PORT is none')

    API_DB_NAME = os.getenv('API_DB_NAME')
    if not API_DB_NAME:
        logger.warning('API_DB_NAME is none')

    API_DB_USE_SSL = os.getenv('API_DB_USE_SSL')
    if not API_DB_USE_SSL:
        logger.warning('API_DB_USE_SSL is none, use False by default')
        API_DB_USE_SSL = False
    API_DB_USE_SSL = bool(API_DB_USE_SSL)

    API_DEBUG_MODE = os.getenv('API_DEBUG_MODE')
    if not API_DEBUG_MODE:
        logger.warning('API_DEBUG_MODE is none, use False by default')
        API_DEBUG_MODE = False
    API_DEBUG_MODE = bool(API_DEBUG_MODE)

    return Config(
        API_PORT=API_PORT,
        API_DB_USER=API_DB_USER,
        API_DB_PASSWORD=API_DB_PASSWORD,
        API_DB_HOST=API_DB_HOST,
        API_DB_PORT=API_DB_PORT,
        API_DB_NAME=API_DB_NAME,
        API_DB_USE_SSL=API_DB_USE_SSL,
        API_DEBUG_MODE=API_DEBUG_MODE,
    )
