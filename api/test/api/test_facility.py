from aiohttp.test_utils import ClientSession


async def test_facility_create(cli: ClientSession):
    # Успешное создание пользователя
    create_user_data = {
        'email': 'user@example.com',
        'password': 'hackme'
    }
    resp = await cli.post('/admin/users', data=create_user_data)
    assert resp.status == 201

    # Успешная аутентификация
    resp = await cli.post('/admin/login', data=create_user_data)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data.get('access_token')
    assert resp_data.get('refresh_token')

    access_token = resp_data.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Успешное создание объекта
    facility1 = {
        'name': 'gym next door 1',
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
    }
    resp = await cli.post('/facility', data=facility1, headers=headers)
    assert resp.status == 201
    assert (await resp.json()).get('id') is not None

    # Неудачное создание объекта (неправильный enum)
    facility3 = {
        'name': 'gym next door 2',
        'x': 123,
        'y': 456,
        'type': 'INVALID',
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
    }
    resp = await cli.post('/facility', data=facility3, headers=headers)
    assert resp.status == 422
    assert (await resp.json()).get('message') == 'validation error'

    # Неудачное создание объекта (без полей x, y)
    facility2 = {
        'name': 'gym next door 2',
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
    }
    resp = await cli.post('/facility', data=facility2, headers=headers)
    assert resp.status == 422
    assert (await resp.json()).get('message') == 'validation error'


async def test_facility_update(cli: ClientSession):
    # Успешное создание пользователя
    create_user_data = {
        'email': 'user@example.com',
        'password': 'hackme'
    }
    resp = await cli.post('/admin/users', data=create_user_data)
    assert resp.status == 201

    # Успешная аутентификация
    resp = await cli.post('/admin/login', data=create_user_data)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data.get('access_token')
    assert resp_data.get('refresh_token')

    access_token = resp_data.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Успешное создание объекта
    facility1 = {
        'name': 'gym next door 1',
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
    }
    resp = await cli.post('/facility', data=facility1, headers=headers)
    assert resp.status == 201
    created_facility_id = (await resp.json()).get('id')
    assert created_facility_id is not None

    resp = await cli.put('/facility/INVALID', data={'x': 65536}, headers=headers)
    assert resp.status == 400

    resp = await cli.put(f'/facility/{created_facility_id}', data={'x': 65536})
    assert resp.status == 401

    # Успешное обновление объекта
    resp = await cli.put(f'/facility/{created_facility_id}', data={'x': 65536}, headers=headers)
    assert resp.status == 200
    resp_json = await resp.json()
    updated_facility_id = resp_json.get('id')
    updated_facility_x = resp_json.get('x')
    assert updated_facility_id == created_facility_id
    assert updated_facility_x != facility1['x']
    assert updated_facility_x == 65536


async def test_facility_hide(cli: ClientSession):
    # создание пользователя
    create_user_data = {
        'email': 'user@example.com',
        'password': 'hackme'
    }
    resp = await cli.post('/admin/users', data=create_user_data)
    # аутентификация
    resp = await cli.post('/admin/login', data=create_user_data)
    resp_data = await resp.json()
    access_token = resp_data.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # создание объекта
    facility1 = {
        'name': 'gym next door 1',
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
    }
    resp = await cli.post('/facility', data=facility1, headers=headers)
    created_facility_id = (await resp.json()).get('id')

    resp = await cli.patch(f'/facility/{created_facility_id}', data={"hidden": True})
    assert resp.status == 401

    resp = await cli.patch('/facility/INVALID', data={"hidden": True}, headers=headers)
    assert resp.status == 400

    resp = await cli.patch(f'/facility/{created_facility_id}', data={"hidden": True}, headers=headers)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data.get('hidden')


async def test_facility_delete(cli: ClientSession):
    # Успешное создание пользователя
    create_user_data = {
        'email': 'user@example.com',
        'password': 'hackme'
    }
    resp = await cli.post('/admin/users', data=create_user_data)
    assert resp.status == 201

    # Успешная аутентификация
    resp = await cli.post('/admin/login', data=create_user_data)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data.get('access_token')
    assert resp_data.get('refresh_token')

    access_token = resp_data.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Успешное создание объекта
    facility1 = {
        'name': 'gym next door 1',
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
    }
    resp = await cli.post('/facility', data=facility1, headers=headers)
    assert resp.status == 201
    created_facility_id = (await resp.json()).get('id')
    assert created_facility_id is not None

    resp = await cli.delete('/facility/INVALID', headers=headers)
    assert resp.status == 400

    # Успешное удаление объекта
    resp = await cli.delete(f'/facility/{created_facility_id}', headers=headers)
    assert resp.status == 204

    # Снова создание объекта, чтобы проверить, как там удаление
    facility1 = {
        'name': 'gym next door 1',
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
    }
    resp = await cli.post('/facility', data=facility1, headers=headers)
    assert resp.status == 201
    created_facility_id = (await resp.json()).get('id')
    assert created_facility_id is not None


async def test_facility_get_by_id(cli: ClientSession):
    # Успешное создание пользователя
    create_user_data = {
        'email': 'user@example.com',
        'password': 'hackme'
    }
    resp = await cli.post('/admin/users', data=create_user_data)
    assert resp.status == 201

    # Успешная аутентификация
    resp = await cli.post('/admin/login', data=create_user_data)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data.get('access_token')
    assert resp_data.get('refresh_token')

    access_token = resp_data.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Успешное создание объекта
    facility1 = {
        'name': 'gym next door 1',
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
    }
    resp = await cli.post('/facility', data=facility1, headers=headers)
    assert resp.status == 201
    created_facility_id = (await resp.json()).get('id')
    assert created_facility_id is not None

    # Неудачное получение объекта
    resp = await cli.get('/facility/ololol', headers=headers)
    assert resp.status == 400

    # Успешное получение объекта
    resp = await cli.get(f'/facility/{created_facility_id}', headers=headers)
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json.get('id') == created_facility_id
    assert resp_json.get('name') == facility1['name']


async def test_facility_get_all(cli: ClientSession):
    # Успешное создание пользователя
    create_user_data = {
        'email': 'user@example.com',
        'password': 'hackme'
    }
    resp = await cli.post('/admin/users', data=create_user_data)
    assert resp.status == 201

    # Успешная аутентификация
    resp = await cli.post('/admin/login', data=create_user_data)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data.get('access_token')
    assert resp_data.get('refresh_token')

    access_token = resp_data.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Успешное создание объекта
    facility1 = {
        'name': 'gym next door 1',
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
    }
    resp = await cli.post('/facility', data=facility1, headers=headers)
    assert resp.status == 201
    created_facility_id = (await resp.json()).get('id')
    assert created_facility_id is not None

    # Успешное получение объектов
    resp = await cli.get('/facility', headers=headers)
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json.get('count') == 1
    for k in facility1:
        assert k in resp_json.get('data')[0]


async def test_facility_search(cli: ClientSession):
    # Успешное создание пользователя
    create_user_data = {
        'email': 'user@example.com',
        'password': 'hackme'
    }
    resp = await cli.post('/admin/users', data=create_user_data)
    assert resp.status == 201

    # Успешная аутентификация
    resp = await cli.post('/admin/login', data=create_user_data)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data.get('access_token')
    assert resp_data.get('refresh_token')

    access_token = resp_data.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Успешное создание объекта
    facility1 = {
        'name': 'gym next door 1',
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
    }
    resp = await cli.post('/facility', data=facility1, headers=headers)
    assert resp.status == 201
    created_facility_id = (await resp.json()).get('id')
    assert created_facility_id is not None

    # Успешный поиск
    resp = await cli.post('/facility/search', data={
        "offset": 0,
        "limit": 10,
        "order_by": "name",
        "filters": [
            {
                "eq": "OOO Gachimuchi Corp.",
                "field": "owner_name"
            }
        ]
    }, headers=headers)
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json.get('count') == 1
    for k in facility1:
        assert k in resp_json.get('data')[0]
