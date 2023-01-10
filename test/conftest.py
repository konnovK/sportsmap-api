import asyncio

import pytest

from api_config import get_config
from db.schema import metadata
from db.utils import get_db_engine


@pytest.fixture()
def loop():
    return asyncio.get_event_loop()


@pytest.fixture()
async def setup_db(loop):
    config = get_config()
    engine = await get_db_engine(config)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
