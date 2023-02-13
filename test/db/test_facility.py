import random

from sqlalchemy.ext.asyncio import AsyncSession

from db import Facility


async def test_search(setup_db):
    async with setup_db() as session:
        session: AsyncSession
        await session.begin()

        for i in range(1, 1001):
            f = Facility(**{
                'name': f'gym {i}',
                'x': random.randint(1, 100),
                'y': 456,
            })
            session.add(f)

        fs = await Facility.search(
            session,
            offset=0,
            limit=20,
            order_by='name',
            order_desc=False,
            filters=[
                {
                    'field': 'name',
                    'eq': 'gym 1',
                },
                {
                    'field': 'x',
                    'lt': 64,
                    'gt': 50
                }
            ]
        )
        print(fs)  #

        await session.rollback()
