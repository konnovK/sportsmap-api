import ssl

from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api_config import Config


async def setup_db(app: web.Application, config: Config):
    db_conn_str = config.API_DB_URL
    connect_args = {}
    if config.API_DB_USE_SSL:
        connect_args["ssl"] = ssl.create_default_context(cafile='./CA.pem')

    engine = create_async_engine(
        db_conn_str,
        connect_args=connect_args,
        pool_size=20,
        max_overflow=60
    )

    Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    app['session'] = Session

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
