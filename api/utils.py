import ssl

import logging

from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


async def setup_db(app: web.Application, settings):
    db_conn_str = settings.API_DB_URL
    connect_args = {}
    if settings.API_DB_USE_SSL:
        connect_args["ssl"] = ssl.create_default_context(cafile='./CA.pem')

    engine = create_async_engine(
        db_conn_str,
        connect_args=connect_args,
        pool_size=20,
        max_overflow=60
    )

    Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    app['sessionmaker'] = Session

    try:
        yield
    finally:
        await engine.dispose()


def hash_password(password: str | None) -> str | None:
    """
    Хеширование пароля.
    :param password: пароль
    :return: sha256 хеш от пароля
    """
    if password is None:
        return None
    from hashlib import sha256
    return sha256(str(password).encode()).hexdigest()


def setup_logger(logger: logging.Logger):
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
