async def test_ping(cli):
    resp = await cli.get('/ping')
    assert resp.status == 200
    assert (await resp.json())['ping'] == 'pong'


async def test_auth_ping(cli):
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

    resp = await cli.get('/authping', headers=headers)
    assert resp.status == 200
    assert (await resp.json())['ping'] == 'pong'


async def test_unknown_url(cli):
    resp = await cli.get('/invalidurl')
    assert resp.status == 404
