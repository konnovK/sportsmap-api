import asyncio
import ssl

import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from api.app import create_app
from api_config import get_config
from db.schema import metadata


@pytest.fixture()
def loop():
    return asyncio.get_event_loop()


@pytest.fixture()
async def setup_db(loop):
    config = get_config()
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
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture()
async def connection(loop, setup_db):
    engine = setup_db
    async with engine.begin() as conn:
        yield conn


@pytest.fixture
def cli(loop, aiohttp_client, setup_db):
    config = get_config()
    app = create_app(config)
    return loop.run_until_complete(aiohttp_client(app))
