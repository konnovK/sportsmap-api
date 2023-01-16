from db.data.facility import Facility, FacilityMapper


async def test_facility_create(connection):
    conn = connection
    facility_mapper = FacilityMapper(conn)

    # Создание обычного объекта
    facility = Facility.new(**{
        'name': 'obj1',
        'x': 123,
        'y': 456,
        'type': 'Gym',
    })
    inserted_facility_id = await facility_mapper.save(facility)
    assert inserted_facility_id is not None

    # Создание объекта, который уже должен существовать
    updated_facility_id = await facility_mapper.save(facility)
    assert updated_facility_id is None
