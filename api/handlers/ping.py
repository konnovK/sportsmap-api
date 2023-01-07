from aiohttp import web
from aiohttp_apispec import (
    docs,
)


@docs(
    tags=["Health check"],
    summary="Пинг сервера",
    description="Пинг, чтобы проверить, что сервер жив.",
)
async def ping_handler(request: web.Request) -> web.Response:
    return web.json_response({'ping': 'pong'})


@docs(
    tags=["Health check"],
    summary="Пинг сервера с авторизацией",
    description="Тот же пинг, но нужно быть авторизованным.",
)
async def auth_ping_handler(request: web.Request) -> web.Response:
    return web.json_response({'ping': 'pong'})
