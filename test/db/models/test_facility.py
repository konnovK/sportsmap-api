from db.data.facility import Facility, FacilityMapper


async def test_facility_create(connection):
    conn = connection
    facility_mapper = FacilityMapper(conn)

    # Создание обычного объекта
    # facility = Facility.new(**{
    #     'name': 'obj1',
    #     'x': 123,
    #     'y': 456,
    #     'type': 'Gym',
    # })
    facility1 = Facility.new(**{
        'name': 'gym next door',
        'x': 123,
        'y': 456,
        'type': 'Gym',
        'owner_name': 'OOO Gachimuchi Corp.',
        'property_form': 'Private',
        'length': 128,
        'width': 32,
        'area': 128 * 32,
        'actual_workload': 123,
        'annual_capacity': 456,
        'notes': 'Для настоящих пацанов',
        'height': 43,
        'size': 12345,
        'depth': 12,
        'converting_type': 'RubberBitumen',
        'is_accessible_for_disabled': True,
        'paying_type': 'PartlyFree',
        'who_can_use': 'Настоящие пацаны',
        'link': 'https://sportsmap.spb.ru',
        'phone_number': '88005553535',
        'open_hours': 'Круглосуточно',
        'eps': 12345,
        'hidden': False,
    })
    inserted_facility_id = await facility_mapper.save(facility1)
    assert inserted_facility_id is not None

    # Создание объекта, который уже должен существовать
    updated_facility_id = await facility_mapper.save(facility1)
    assert updated_facility_id is None

    # Создание простого объекта
    facility2 = Facility.new(**{
        'name': 'obj1',
        'x': 123,
        'y': 456,
        'type': 'Gym',
    })
    inserted_facility_id = await facility_mapper.save(facility2)
    assert inserted_facility_id is not None


async def test_facility_delete(connection):
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

    # Удаление простого пользователя
    await facility_mapper.delete(facility)

    inserted_facility_id = await facility_mapper.save(facility)
    assert inserted_facility_id is not None


async def test_facility_get(connection):
    conn = connection
    facility_mapper = FacilityMapper(conn)

    assert await facility_mapper.get_by_id('INVALID') is None

    # Создание обычного объекта
    facility = Facility.new(**{
        'name': 'obj1',
        'x': 123,
        'y': 456,
        'type': 'Gym',
    })
    inserted_facility_id = await facility_mapper.save(facility)
    assert inserted_facility_id is not None

    facility_get = await facility_mapper.get_by_id(facility.id)
    assert facility_get is not None
    assert hasattr(facility_get, 'id')
    assert hasattr(facility_get, 'x')
    assert hasattr(facility_get, 'y')
    assert hasattr(facility_get, 'type')
    assert hasattr(facility_get, 'owner_name')
    assert hasattr(facility_get, 'property_form')
    assert hasattr(facility_get, 'length')
    assert hasattr(facility_get, 'width')
    assert hasattr(facility_get, 'area')
    assert hasattr(facility_get, 'actual_workload')
    assert hasattr(facility_get, 'annual_capacity')
    assert hasattr(facility_get, 'notes')
    assert hasattr(facility_get, 'height')
    assert hasattr(facility_get, 'size')
    assert hasattr(facility_get, 'depth')
    assert hasattr(facility_get, 'converting_type')
    assert hasattr(facility_get, 'is_accessible_for_disabled')
    assert hasattr(facility_get, 'paying_type')
    assert hasattr(facility_get, 'who_can_use')
    assert hasattr(facility_get, 'link')
    assert hasattr(facility_get, 'phone_number')
    assert hasattr(facility_get, 'open_hours')
    assert hasattr(facility_get, 'eps')
    assert hasattr(facility_get, 'hidden')
