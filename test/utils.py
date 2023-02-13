async def check_ok(resp, status: int, fields: list[str]):
    result = await resp.json()
    assert resp.status == status
    for f in fields:
        assert f in result


async def check_validation_error(resp):
    result = await resp.json()
    assert resp.status == 422
    assert 'message' in result
    assert 'detail' in result
    assert result['message'] == 'validation error'


async def check_error(resp, status: int, message: str):
    result = await resp.json()
    assert resp.status == status
    assert 'message' in result
    assert 'detail' in result
    assert result['message'] == message


async def get_token(cli, email, password):
    resp = await cli.post('/admin/login', data={
        'email': email,
        'password': password
    })
    resp_data = await resp.json()
    access_token = resp_data.get('access_token')
    refresh_token = resp_data.get('refresh_token')
    return access_token, refresh_token


async def auth(cli, email, password):
    access_token, _ = await get_token(cli, email, password)
    return {
        'Authorization': f'Bearer {access_token}'
    }
