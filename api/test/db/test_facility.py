# import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from db import Facility


async def test_search(setup_db):
    async with setup_db() as session:
        session: AsyncSession
        await session.begin()

        for i in range(1, 1001):
            f = Facility(**{
                'name': f'gym {i}',
                'x': 123,
                'y': 456,
            })
            session.add(f)

        fs = await Facility.search(
            session,
            # offset=10,
            limit=10,
            sort_by='id',
            sort_desc=True,
            fields={
                'name': 'gym 666',
                'x': 123,
            }
        )
        print(fs)  #

        await session.rollback()
