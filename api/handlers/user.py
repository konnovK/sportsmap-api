from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
)

from api.jwt import create_jwt, get_email_from_access_token, refresh_jwt
from api.schemas.error import ErrorResponse
from api.schemas.user import UserResponse, CreateUserRequest, LoginRequest, LoginResponse, RefreshTokenRequest
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
        user_id = await User.create_user(conn, user_first_name, user_last_name, user_email, user_password)

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
            raise web.HTTPException(text='wrong email or password')

    access_token, refresh_token, expires_in = create_jwt(user.email)

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

    user_email = get_email_from_access_token(access_token)
    if not user_email:
        raise web.HTTPException(text='wrong access token')

    async with request.app['db'].begin() as conn:
        user = await User.get_by_email(conn, user_email)
        if not user:
            raise web.HTTPException(text='wrong access token')

    access_token, refresh_token, expires_in = refresh_jwt(access_token, refresh_token)
    if access_token is None:
        raise web.HTTPException(text='wrong refresh token')

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
async def delete_self(request: web.Request) -> web.Response:
    user_email = request.app['email']
    async with request.app['db'].begin() as conn:
        user = await User.get_by_email(conn, user_email)
        if not user:
            raise web.HTTPException(text='user with this email not found')
        await User.delete_by_email(conn, user_email)
    return web.json_response(status=204)
