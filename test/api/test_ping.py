from test import utils


async def test_ping(cli):
    resp = await cli.get('/ping')
    assert resp.status == 200
    assert (await resp.json())['ping'] == 'pong'


async def test_auth_ping(cli):
    # аутентификация
    await cli.post('/admin/users', data={
        'email': 'user@example.com',
        'password': 'hackme'
    })
    headers = await utils.auth(cli, 'user@example.com', 'hackme')

    resp = await cli.get('/authping', headers=headers)
    assert resp.status == 200
    assert (await resp.json())['ping'] == 'pong'


async def test_unknown_url(cli):
    resp = await cli.get('/invalidurl')
    assert resp.status == 404
