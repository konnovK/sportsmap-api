import ssl

from api_config import Config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
import sqlalchemy as sa
from aiohttp import web
from loguru import logger


async def get_db_engine(config: Config) -> AsyncEngine:
    """
     Получение sqlalchemy async engine, исходя из содержания конфига
    """
    logger.info('get sqlalchemy async database engine')
    db_conn_str = f"postgresql+asyncpg://{config.API_DB_USER}:{config.API_DB_PASSWORD}" \
                  f"@{config.API_DB_HOST}:{config.API_DB_PORT}/{config.API_DB_NAME}"

    connect_args = {}
    if config.API_DB_USE_SSL:
        connect_args["ssl"] = ssl.create_default_context(cafile='./CA.pem')

    engine = create_async_engine(
        db_conn_str,
        echo=config.API_DEBUG_MODE,
        connect_args=connect_args
    )

    async with engine.begin() as conn:
        await conn.execute(sa.select(1))

    return engine


async def setup_db(app: web.Application, config: Config):
    """
     Подключение к БД и отключение от БД для приложения
    """
    logger.info('connecting API to DB')
    engine = await get_db_engine(config)
    app['db'] = engine
    logger.info('connected API to DB successfully')
    try:
        yield
    finally:
        logger.info('disconnect API from DB')
        await app['db'].dispose()
        logger.info('disconnected API from DB successfully')


async def debug_db_init(config: Config):
    """
     Полная очистка бд для режима дебага
    """
    if not config.API_DEBUG_MODE:
        return
    engine = await get_db_engine(config)
    from db.schema import metadata
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        # await conn.run_sync(metadata.create_all)


def hash_password(password: str) -> str:
    """
    Хеширование пароля.
    :param password: пароль
    :return: sha256 хеш от пароля
    """
    from hashlib import sha256
    return sha256(str(password).encode()).hexdigest()
