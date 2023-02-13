import pytest
from aiohttp.test_utils import ClientSession
from test import utils


@pytest.mark.parametrize('request_data', [
    {
        'email': 'user@example.com',
        'password': 'hackme',
        'first_name': 'kirill',
        'last_name': 'konnov'
    },
    {
        'email': 'user@example.com',
        'password': 'hackme',
    }
])
async def test_user_create_success(cli: ClientSession, request_data):
    resp = await cli.post('/admin/users', data=request_data)
    await utils.check_ok(resp, 201, ['id', 'email'])


@pytest.mark.parametrize('request_data', [
    {
        'email': 'bad email',
        'password': 'hackme',
        'first_name': 'kirill',
        'last_name': 'konnov'
    },
    {
        'email': 'user@example.com',
        'password': 'hackme',
        'INVALID': 'INVALID'
    },
    {
        'email': 'user@example.com',
    },
])
async def test_user_create_bad_validation(cli: ClientSession, request_data):
    resp = await cli.post('/admin/users', data=request_data)
    await utils.check_validation_error(resp)


@pytest.mark.parametrize('request_data', [
    {
        'email': 'user@example.com',
        'password': 'hackme',
        'first_name': 'kirill',
        'last_name': 'konnov'
    }
])
async def test_user_create_already_exists(cli: ClientSession, request_data):
    resp = await cli.post('/admin/users', data=request_data)
    await utils.check_ok(resp, 201, ['id', 'email'])
    resp = await cli.post('/admin/users', data=request_data)
    await utils.check_error(resp, 409, 'user already exists')


@pytest.mark.parametrize('request_data', [
    {
        'email': 'user@example.com',
        'password': 'hackme',
    }
])
async def test_user_login_success(cli: ClientSession, request_data):
    # Создание пользователя
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    # Аутентификация
    resp = await cli.post('/admin/login', data=request_data)
    await utils.check_ok(resp, 200, ['access_token_expires_in', 'access_token', 'refresh_token'])


@pytest.mark.parametrize('request_data', [
    {
        'email': 'INVALID',
        'password': 'hackme',
    },
    {
        'email': 'INVALID',
    },
    {
        'email': 'user@example.com',
        'password': 'hackme',
        'INVALID': 'INVALID'
    },
])
async def test_user_login_bad_validation(cli: ClientSession, request_data):
    # Аутентификация
    resp = await cli.post('/admin/login', data=request_data)
    await utils.check_validation_error(resp)


@pytest.mark.parametrize('request_data', [
    {
        'email': 'user@example.com',
        'password': 'wrong password',
    },
    {
        'email': 'wrong@example.com',
        'password': 'hackme',
    },
])
async def test_user_login_bad_user_data(cli: ClientSession, request_data):
    # Аутентификация
    resp = await cli.post('/admin/login', data=request_data)
    await utils.check_error(resp, 400, 'wrong email or password')


async def test_user_refresh_success(cli: ClientSession):
    # Создание пользователя
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    # Аутентификация
    access_token, refresh_token = await utils.get_token(cli, 'user@example.com', 'hackme')

    # Обновление токена
    resp = await cli.post('/admin/token/refresh', data={
        'access_token': access_token,
        'refresh_token': refresh_token
    })
    await utils.check_ok(resp, 200, ['access_token_expires_in', 'access_token', 'refresh_token'])


async def test_user_refresh_bad_access_token(cli: ClientSession):
    # Создание пользователя
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    # Аутентификация
    access_token, refresh_token = await utils.get_token(cli, 'user@example.com', 'hackme')

    # Обновление токена
    resp = await cli.post('/admin/token/refresh', data={
        'access_token': f'wrong{access_token}',
        'refresh_token': refresh_token
    })
    await utils.check_error(resp, 400, 'wrong access token')


async def test_user_refresh_bad_refresh_token(cli: ClientSession):
    # Создание пользователя
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    # Аутентификация
    access_token, refresh_token = await utils.get_token(cli, 'user@example.com', 'hackme')

    # Обновление токена
    resp = await cli.post('/admin/token/refresh', data={
        'access_token': access_token,
        'refresh_token': f'wrong{refresh_token}'
    })
    await utils.check_error(resp, 400, 'wrong refresh token')


async def test_user_delete_success(cli: ClientSession):
    # Создание пользователя
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    # Аутентификация
    headers = await utils.auth(cli, 'user@example.com', 'hackme')
    # Удаление пользователя
    resp = await cli.delete('/admin/users', headers=headers)
    assert resp.status == 204
    # проверим, что пользователь действительно удалился
    resp = await cli.post('/admin/login', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    await utils.check_error(resp, 400, 'wrong email or password')


@pytest.mark.parametrize('request_headers', [
    {},
    {
        'Authorization': 'INVALID'
    }
])
async def test_user_delete_bad_auth(cli: ClientSession, request_headers):
    # Создание пользователя
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    # Удаление пользователя
    resp = await cli.delete('/admin/users', headers=request_headers)
    assert resp.status == 401


async def test_user_update(cli: ClientSession):
    # Успешное создание пользователя
    create_user_data = {
        'email': 'user@example.com',
        'password': 'hackme',
        'first_name': 'kirill',
        'last_name': 'konnov'
    }
    resp = await cli.post('/admin/users', data=create_user_data)
    assert resp.status == 201

    # Успешная аутентификация
    resp = await cli.post('/admin/login', data={
        'email': 'user@example.com',
        'password': 'hackme',
    })
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data.get('access_token')
    assert resp_data.get('refresh_token')

    access_token = resp_data.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Неправильное изменение пользователя (несуществующее поле)
    resp = await cli.put(
        '/admin/users',
        data={
            'invalid': 'invalid'
        },
        headers=headers
    )
    assert resp.status == 422
    assert (await resp.json()).get('message') == 'validation error'

    # Неправильное изменение пользователя (без токена аутентификации)
    resp = await cli.put(
        '/admin/users',
        data={
            'password': 'qwerty'
        }
    )
    assert resp.status == 401

    # Успешное изменение пользователя
    resp = await cli.put(
        '/admin/users',
        data={
            'first_name': 'ivanov',
            'last_name': 'ivan',
            'password': 'qwerty'
        },
        headers=headers
    )
    assert resp.status == 200

    # Проверим, что пароль действительно изменился
    resp = await cli.post('/admin/login', data={
        'email': create_user_data['email'],
        'password': create_user_data['password']
    })
    assert resp.status == 400
    resp = await cli.post('/admin/login', data={
        'email': create_user_data['email'],
        'password': 'qwerty'
    })
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data.get('access_token')
    assert resp_data.get('refresh_token')


async def test_user_get_by_id(cli: ClientSession):
    # создание пользователя
    create_user_data = {
        'email': 'user@example.com',
        'password': 'hackme',
    }
    resp = await cli.post('/admin/users', data=create_user_data)
    resp_data = await resp.json()
    user_id = resp_data.get('id')
    # аутентификация
    resp = await cli.post('/admin/login', data={
        'email': 'user@example.com',
        'password': 'hackme',
    })
    resp_data = await resp.json()
    access_token = resp_data.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    resp = await cli.get(f'/admin/users/{user_id}')
    await utils.check_error(resp, 401, 'authorization error')

    resp = await cli.get('/admin/users/INVALID', headers=headers)
    await utils.check_error(resp, 400, "user with this id doesn't exists")

    resp = await cli.get(f'/admin/users/{user_id}', headers=headers)
    await utils.check_ok(resp, 200, ['id', 'email', 'first_name', 'last_name'])
