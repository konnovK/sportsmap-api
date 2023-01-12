async def test_ping(cli):
    resp = await cli.get('/ping')
    assert resp.status == 200
    assert (await resp.json())['ping'] == 'pong'
