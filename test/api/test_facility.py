from aiohttp.test_utils import ClientSession

from test import utils


def generate_facility(name: str = 'gym next door 1'):
    facility1 = {
        'name': name,
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
    return facility1


async def test_facility_create(cli: ClientSession):
    # аутентификация
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    headers = await utils.auth(cli, 'user@example.com', 'hackme')

    # Успешное создание объекта
    facility1 = generate_facility('gym next door 1')
    resp = await cli.post('/facility', data=facility1, headers=headers)
    assert resp.status == 201
    assert (await resp.json()).get('id') is not None

    # Неудачное создание объекта (неправильный enum)
    facility3 = generate_facility('gym next door 3')
    facility3['type'] = 'INVALID'

    resp = await cli.post('/facility', data=facility3, headers=headers)
    await utils.check_validation_error(resp)

    # Неудачное создание объекта (без полей x, y)
    facility2 = generate_facility('gym next door 2')
    facility2.pop('x')
    facility2.pop('y')

    resp = await cli.post('/facility', data=facility2, headers=headers)
    await utils.check_validation_error(resp)


async def test_facility_update(cli: ClientSession):
    # аутентификация
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    headers = await utils.auth(cli, 'user@example.com', 'hackme')

    # создание объекта
    facility1 = generate_facility('gym next door 1')
    resp = await cli.post('/facility', data=facility1, headers=headers)
    created_facility_id = (await resp.json()).get('id')

    # Неудачное обновление объекта (неверный id)
    resp = await cli.put('/facility/INVALID', data={'x': 65536}, headers=headers)
    assert resp.status == 400

    # Неудачное обновление объекта (неверный auth токен)
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


async def test_facility_patch(cli: ClientSession):
    # аутентификация
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    headers = await utils.auth(cli, 'user@example.com', 'hackme')

    # создание объекта
    facility1 = generate_facility('gym next door 1')
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
    # аутентификация
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    headers = await utils.auth(cli, 'user@example.com', 'hackme')

    # Успешное создание объекта
    facility1 = generate_facility('gym next door 1')
    resp = await cli.post('/facility', data=facility1, headers=headers)
    created_facility_id = (await resp.json()).get('id')

    resp = await cli.delete('/facility/INVALID', headers=headers)
    assert resp.status == 400

    # Успешное удаление объекта
    resp = await cli.delete(f'/facility/{created_facility_id}', headers=headers)
    assert resp.status == 204

    # Снова создание объекта, чтобы проверить, как там удаление
    facility1 = generate_facility('gym next door 1')
    resp = await cli.post('/facility', data=facility1, headers=headers)
    assert resp.status == 201
    created_facility_id = (await resp.json()).get('id')
    assert created_facility_id is not None


async def test_facility_get_by_id(cli: ClientSession):
    # аутентификация
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    headers = await utils.auth(cli, 'user@example.com', 'hackme')

    # Успешное создание объекта
    facility1 = generate_facility('gym next door 1')
    resp = await cli.post('/facility', data=facility1, headers=headers)
    created_facility_id = (await resp.json()).get('id')

    # Неудачное получение объекта
    resp = await cli.get('/facility/ololol')
    assert resp.status == 400

    # Успешное получение объекта
    resp = await cli.get(f'/facility/{created_facility_id}')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json.get('id') == created_facility_id
    assert resp_json.get('name') == facility1['name']


async def test_facility_get_all(cli: ClientSession):
    # аутентификация
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    headers = await utils.auth(cli, 'user@example.com', 'hackme')

    # Успешное создание объекта
    facility1 = generate_facility('gym next door 1')
    resp = await cli.post('/facility', data=facility1, headers=headers)
    assert resp.status == 201
    created_facility_id = (await resp.json()).get('id')
    assert created_facility_id is not None

    # Успешное получение объектов
    resp = await cli.get('/facility')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json.get('count') == 1
    for k in facility1:
        assert k in resp_json.get('data')[0]


async def test_facility_search(cli: ClientSession):
    # аутентификация
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    headers = await utils.auth(cli, 'user@example.com', 'hackme')

    # Успешное создание объекта
    facility1 = generate_facility('gym next door 1')
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
    })
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json.get('count') == 1
    for k in facility1:
        assert k in resp_json.get('data')[0]

    # Успешный поиск
    resp = await cli.post('/facility/search', data={})
    assert resp.status == 200
