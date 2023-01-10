import asyncio

import pytest

from api_config import get_config
from db.schema import metadata
from db.utils import get_db_engine
from test import TEST_DB_NAME


@pytest.fixture()
def loop():
    return asyncio.get_event_loop()


@pytest.fixture()
async def setup_db(loop):
    config = get_config()
    config.API_DB_USER = 'user123'
    config.API_DB_PASSWORD = '123'
    config.API_DB_HOST = 'localhost'
    config.API_DB_PORT = 5432
    config.API_DB_NAME = TEST_DB_NAME
    engine = await get_db_engine(config)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
