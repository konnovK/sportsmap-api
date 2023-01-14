from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
)

from api.jwt import jwt_middleware, JWTException
from api.schemas.error import ErrorResponse
from api.schemas.user import UserResponse, CreateUserRequest, LoginRequest, LoginResponse, RefreshTokenRequest, \
    UpdateSelfRequest
from db.models.user import User


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
    user_first_name = data.get('first_name')
    user_last_name = data.get('last_name')
    user_email = data.get('email')
    user_password = data.get('password')

    async with request.app['db'].begin() as conn:
        if await User.exists(conn, user_email):
            return web.json_response(status=409)
        user_id = await User.create_user(conn, user_email, user_password, user_first_name, user_last_name)

    return web.json_response(UserResponse().dump({
        "id": user_id,
        "first_name": user_first_name,
        "last_name": user_last_name,
        "email": user_email
    }), status=201)


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
        user = await User.get_by_email_and_password(conn, user_email, user_password)
        if not user:
            raise web.HTTPBadRequest(text='wrong email or password')

    access_token, refresh_token, expires_in = request.app['jwt'].create_jwt(user.email)

    return web.json_response(LoginResponse().dump({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "group": user.group,
        "access_token": access_token,
        "access_token_expires_in": expires_in,
        "refresh_token": refresh_token,
    }))


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
        user = await User.get_by_email(conn, user_email)
        if not user:
            raise web.HTTPBadRequest(text='wrong access token')

    try:
        access_token, refresh_token, expires_in = request.app['jwt'].refresh_jwt(access_token, refresh_token)
    except JWTException:
        raise web.HTTPBadRequest(text='wrong refresh token')
    if access_token is None:
        raise web.HTTPBadRequest(text='wrong refresh token')

    return web.json_response(LoginResponse().dump({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "group": user.group,
        "access_token": access_token,
        "access_token_expires_in": expires_in,
        "refresh_token": refresh_token,
    }))


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
        }
    },
)
@jwt_middleware
async def delete_self(request: web.Request) -> web.Response:
    user_email = request.app['email']
    async with request.app['db'].begin() as conn:
        await User.delete_by_email(conn, user_email)
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
        }
    },
)
@request_schema(UpdateSelfRequest)
@jwt_middleware
async def update_self(request: web.Request) -> web.Response:
    user_email = request.app['email']
    data = UpdateSelfRequest().load(await request.json())

    update_data = {}
    if data.get('first_name'):
        update_data['first_name'] = data.get('first_name')
    if data.get('last_name'):
        update_data['last_name'] = data.get('last_name')
    if data.get('password'):
        update_data['password'] = data.get('password')

    async with request.app['db'].begin() as conn:
        user = await User.update_user(conn, user_email, **update_data)
    return web.json_response(UserResponse().dump({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "group": user.group
    }))
