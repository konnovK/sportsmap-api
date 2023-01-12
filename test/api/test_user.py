from aiohttp.test_utils import ClientSession


async def test_user_create(cli: ClientSession):
    create_user_data = {
        'email': 'user@example.com',
        'password': 'hackme'
    }

    # Успешное создание пользователя
    resp = await cli.post('/admin/users', data=create_user_data)
    assert resp.status == 201

    # Попытка создать уже существуюшего пользователя
    resp = await cli.post('/admin/users', data=create_user_data)
    assert resp.status == 409

    # Отправка данных в некорректной форме
    resp = await cli.post('/admin/users', data={
        'invalid': 'invalid'
    })
    assert resp.status == 400
    resp_data = await resp.json()
    # В ответе 400 есть поля message и detail
    assert resp_data.get('message') == 'validation error'
    assert resp_data.get('detail')


async def test_user_login(cli: ClientSession):
    # Успешное создание пользователя
    create_user_data = {
        'email': 'user@example.com',
        'password': 'hackme'
    }
    resp = await cli.post('/admin/users', data=create_user_data)
    assert resp.status == 201

    # Аутентификация несуществующего пользователя
    resp = await cli.post('/admin/login', data={
        'email': 'invalid@example.com',
        'password': 'hackme'
    })
    assert resp.status == 400
    assert (await resp.json()).get('message') == 'wrong email or password'

    # Аутентификация c неправильным паролем
    resp = await cli.post('/admin/login', data={
        'email': 'user@example.com',
        'password': 'hackme23'
    })
    assert resp.status == 400
    assert (await resp.json()).get('message') == 'wrong email or password'

    # Успешная аутентификация
    resp = await cli.post('/admin/login', data=create_user_data)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data.get('access_token')
    assert resp_data.get('refresh_token')


async def test_user_refresh(cli: ClientSession):
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
    assert resp_data.get('access_token_expires_in')

    access_token = resp_data.get('access_token')
    refresh_token = resp_data.get('refresh_token')

    # Неудачное обновление токена (плохой access_token)
    resp = await cli.post('/admin/token/refresh', data={
        'access_token': access_token + 'invalid',
        'refresh_token': refresh_token
    })
    assert resp.status == 400
    assert (await resp.json()).get('message') == 'wrong access token'

    # Неудачное обновление токена (плохой refresh_token)
    resp = await cli.post('/admin/token/refresh', data={
        'access_token': access_token,
        'refresh_token': refresh_token + 'invalid'
    })
    assert resp.status == 400
    assert (await resp.json()).get('message') == 'wrong refresh token'

    # Успешное обновление токена
    resp = await cli.post('/admin/token/refresh', data={
        'access_token': access_token,
        'refresh_token': refresh_token
    })
    assert resp.status == 200
    assert resp_data.get('access_token')
    assert resp_data.get('refresh_token')
    assert resp_data.get('access_token_expires_in')


async def test_user_update(cli: ClientSession):
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

    # Неправильное изменение пользователя (несуществующее поле)
    resp = await cli.put(
        '/admin/users',
        data={
            'invalid': 'invalid'
        },
        headers=headers
    )
    assert resp.status == 400
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
            'password': 'qwerty'
        },
        headers=headers
    )
    assert resp.status == 200

    # Проверим, что пароль действительно изменился
    resp = await cli.post('/admin/login', data=create_user_data)
    assert resp.status == 400
    resp = await cli.post('/admin/login', data={
        'email': create_user_data['email'],
        'password': 'qwerty'
    })
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data.get('access_token')
    assert resp_data.get('refresh_token')


async def test_user_delete(cli: ClientSession):
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

    # Неудальное удаление пользователя (без аутентификации)
    resp = await cli.delete('/admin/users')
    assert resp.status == 401

    # Успешное удаление пользователя
    resp = await cli.delete('/admin/users', headers=headers)
    assert resp.status == 204

    # проверим, что пользователь действительно удалился
    resp = await cli.post('/admin/login', data=create_user_data)
    assert resp.status == 400
    assert (await resp.json())['message'] == 'wrong email or password'
