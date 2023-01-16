from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
)

from api.jwt import jwt_middleware, JWTException
from api.schemas.error import ErrorResponse
from api.schemas.user import UserResponse, CreateUserRequest, LoginRequest, LoginResponse, RefreshTokenRequest, \
    UpdateSelfRequest
from db.data.user import User, UserMapper


@docs(
    tags=["Admin"],
    summary="Создание пользователя",
    description="Регистрация. Создание нового пользователя.",
    responses={
        201: {
            "schema": UserResponse,
            "description": "Пользователь успешно создан"
        },
        400: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации входных данных"
        },
        409: {
            "description": "Пользователь с таким email уже существует"
        }
    },
)
@request_schema(CreateUserRequest)
async def register(request: web.Request) -> web.Response:
    data = CreateUserRequest().load(await request.json())
    user = User.new(**data)

    async with request.app['db'].begin() as conn:
        user_mapper = UserMapper(conn)

        if await user_mapper.get_by_email(user.email):
            return web.json_response(status=409)
        await user_mapper.save(user)

    return web.json_response(UserResponse().dump(user), status=201)


@docs(
    tags=["Admin"],
    summary="Аутентификация",
    description="Аутентификация, получение jwt токена.",
    responses={
        200: {
            "schema": LoginResponse,
            "description": "Успешная аутентификация"
        },
        400: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации, Неверный email или пароль"
        }
    },
)
@request_schema(LoginRequest)
async def login(request: web.Request) -> web.Response:
    data = LoginRequest().load(await request.json())
    user_email = data.get('email')
    user_password = data.get('password')

    async with request.app['db'].begin() as conn:
        user_mapper = UserMapper(conn)

        user = await user_mapper.get_by_email_and_password(user_email, user_password)
        if user is None:
            raise web.HTTPBadRequest(text='wrong email or password')

    access_token, refresh_token, expires_in = request.app['jwt'].create_jwt(user.email)

    return web.json_response({
        "access_token": access_token,
        "access_token_expires_in": expires_in,
        "refresh_token": refresh_token,
        **LoginResponse().dump(user)
    })


@docs(
    tags=["Admin"],
    summary="Получить новый токен",
    description="Обновление jwt токена по access_token, refresh_token.",
    responses={
        200: {
            "schema": LoginResponse,
            "description": "Успешное обновление токена"
        },
        400: {
            "schema": ErrorResponse,
            "description": "Невалидный токен"
        }
    },
)
@request_schema(RefreshTokenRequest)
async def refresh_token(request: web.Request) -> web.Response:
    data = RefreshTokenRequest().load(await request.json())
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')

    try:
        user_email = request.app['jwt'].get_email_from_access_token(access_token)
    except JWTException:
        raise web.HTTPBadRequest(text='wrong access token')
    if not user_email:
        raise web.HTTPBadRequest(text='wrong access token')

    async with request.app['db'].begin() as conn:
        user_mapper = UserMapper(conn)

        user = await user_mapper.get_by_email(user_email)
        if user is None:
            raise web.HTTPBadRequest(text='wrong access token')

    try:
        access_token, refresh_token, expires_in = request.app['jwt'].refresh_jwt(access_token, refresh_token)
    except JWTException:
        raise web.HTTPBadRequest(text='wrong refresh token')

    if access_token is None:
        raise web.HTTPBadRequest(text='wrong refresh token')

    return web.json_response({
        "access_token": access_token,
        "access_token_expires_in": expires_in,
        "refresh_token": refresh_token,
        **LoginResponse().dump(user)
    })


@docs(
    tags=["Admin"],
    summary="Удалить себя",
    description="Удаление себя. Требуется аутентификация.",
    responses={
        204: {
            "description": "Успешное удаление"
        },
        400: {
            "schema": ErrorResponse,
            "description": "Ошибка входных данных (незнаю, каких именно, например, если прислали неправильный токен)"
        },
        401: {
            "description": "Ошибка аутентификации (отсутствующий или неправильный токен аутентификации. "
                           "Authorization: Bearer 'текст токена') "
        },
    },
)
@jwt_middleware
async def delete_self(request: web.Request) -> web.Response:
    user = request.app['user']

    async with request.app['db'].begin() as conn:
        user_mapper = UserMapper(conn)

        await user_mapper.delete(user)

    return web.json_response(status=204)


@docs(
    tags=["Admin"],
    summary="Обновить инфу о себе",
    description="Обновить инфу о себе. Требуется аутентификация.",
    responses={
        200: {
            "schema": UserResponse,
            "description": "Пользователь успешно обновлен"
        },
        400: {
            "schema": ErrorResponse,
            "description": "Ошибка входных данных"
        },
        401: {
            "description": "Ошибка аутентификации (отсутствующий или неправильный токен аутентификации. "
                           "Authorization: Bearer 'текст токена') "
        },
    },
)
@request_schema(UpdateSelfRequest)
@jwt_middleware
async def update_self(request: web.Request) -> web.Response:
    user = request.app['user']

    data = UpdateSelfRequest().load(await request.json())

    if data.get('first_name'):
        user.first_name = data.get('first_name')
    if data.get('last_name'):
        user.last_name = data.get('last_name')
    if data.get('password'):
        user.set_password(data.get('password'))

    async with request.app['db'].begin() as conn:
        user_mapper = UserMapper(conn)

        user = await user_mapper.save(user)

    return web.json_response(UserResponse().dump(user))
