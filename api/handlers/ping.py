from aiohttp import web
from aiohttp_apispec import (
    docs,
)

from api.jwt import jwt_middleware


@docs(
    tags=["Health check"],
    summary="Пинг сервера",
    description="Пинг, чтобы проверить, что сервер жив.",
    responses={
        200: {
            "description": "Успешно"
        },
    },
)
async def ping_handler(request: web.Request) -> web.Response:
    return web.json_response({'ping': 'pong'})


@docs(
    tags=["Health check"],
    summary="Пинг сервера с авторизацией",
    description="Тот же пинг, но нужно быть авторизованным.",
    responses={
        200: {
            "description": "Успешно"
        },
        401: {
            "description": "Ошибка аутентификации (отсутствующий или неправильный токен аутентификации. "
                           "Authorization: Bearer 'текст токена') "
        },
    },
)
@jwt_middleware
async def auth_ping_handler(request: web.Request) -> web.Response:
    return web.json_response({'ping': 'pong'})
