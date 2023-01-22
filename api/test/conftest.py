import asyncio
import ssl

import pytest
from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.app import create_app
from api_config import Config
from db.schema import metadata


@pytest.fixture()
def loop():
    return asyncio.get_event_loop()


@pytest.fixture()
async def setup_db(loop):
    config = Config.new()
    db_conn_str = config.API_DB_URL
    connect_args = {}
    if config.API_DB_USE_SSL:
        connect_args["ssl"] = ssl.create_default_context(cafile='./CA.pem')

    engine = create_async_engine(
        db_conn_str,
        connect_args=connect_args
    )
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield Session

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture
def cli(loop, aiohttp_client, setup_db):
    config = Config.new()
    app: web.Application = create_app(config)

    app.cleanup_ctx.pop()
    app['sessionmaker'] = setup_db

    return loop.run_until_complete(aiohttp_client(app))
