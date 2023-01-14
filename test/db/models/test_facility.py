import pytest

from db.models.facility import Facility


class TestUser:
    @pytest.mark.asyncio
    async def test_facility_create(self, setup_db):
        engine = setup_db

        created_facility = {
            'name': 'obj1',
            'x': 123,
            'y': 456,
            'type': 'Gym',
        }

        async with engine.begin() as conn:
            assert not await Facility.exists(conn, created_facility['name'])
            await Facility.create(conn, created_facility)
            assert await Facility.exists(conn, created_facility['name'])
