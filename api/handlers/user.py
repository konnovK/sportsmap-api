import logging

from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
)
from sqlalchemy.exc import IntegrityError, DBAPIError

from db import User
from api.jwt import JWTException, jwt_check  # , JWTException
from api.schemas.error import ErrorResponse
from api.schemas.user import (
    UserResponse,
    CreateUserRequest,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    UpdateSelfRequest
)
from utils import setup_logger

logger = logging.getLogger(__name__)
setup_logger(logger)


@docs(
    tags=["Admin"],
    summary="Создание пользователя",
    description="Регистрация. Создание нового пользователя.",
    responses={
        201: {
            "schema": UserResponse,
            "description": "Пользователь успешно создан"
        },
        409: {
            "description": "Пользователь с таким email уже существует"
        },
        422: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации входных данных"
        },
    },
)
@request_schema(CreateUserRequest)
async def register(request: web.Request) -> web.Response:
    data = CreateUserRequest().load(await request.json())
    user = User(**data)

    session = request['session']
    try:
        session.add(user)
        await session.flush()
    except IntegrityError:
        raise web.HTTPConflict(text='user already exists')

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
            "description": "Неверный email или пароль"
        },
        422: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации входных данных"
        },
    },
)
@request_schema(LoginRequest)
async def login(request: web.Request) -> web.Response:
    data = LoginRequest().load(await request.json())
    user_email = data.get('email')
    user_password = data.get('password')

    session = request['session']

    existed_user = await User.get_by_email_and_password(session, user_email, user_password)
    if existed_user is None:
        raise web.HTTPBadRequest(text='wrong email or password')

    access_token, refresh_token, expires_in = request.app['jwt'].create_jwt(existed_user.email)

    return web.json_response({
        "access_token": access_token,
        "access_token_expires_in": expires_in,
        "refresh_token": refresh_token,
        **UserResponse().dump(existed_user)
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
        },
        422: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации входных данных"
        },
    },
)
@request_schema(RefreshTokenRequest)
async def refresh_token(request: web.Request) -> web.Response:
    data = RefreshTokenRequest().load(await request.json())
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')

    session = request['session']

    try:
        user_email = request.app['jwt'].get_email_from_access_token(access_token)
    except JWTException:
        raise web.HTTPBadRequest(text='wrong access token')
    if not user_email:
        raise web.HTTPBadRequest(text='wrong access token')

    user = await User.get_by_email(session, user_email)
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
        401: {
            "description": "Ошибка аутентификации (отсутствующий или неправильный токен аутентификации. "
                           "Authorization: Bearer 'текст токена') "
        },
        422: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации входных данных"
        },
    },
)
async def delete_self(request: web.Request) -> web.Response:
    jwt_check(request)
    user_email = request['email']

    session = request['session']

    user = await User.get_by_email(session, user_email)
    await session.delete(user)

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
        401: {
            "description": "Ошибка аутентификации (отсутствующий или неправильный токен аутентификации. "
                           "Authorization: Bearer 'текст токена') "
        },
        422: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации входных данных"
        },
    },
)
@request_schema(UpdateSelfRequest)
async def update_self(request: web.Request) -> web.Response:
    jwt_check(request)
    user_email = request['email']
    data = UpdateSelfRequest().load(await request.json())

    session = request['session']

    user = await User.get_by_email(session, user_email)
    if user is None:
        return web.HTTPBadRequest(text='unknown user email')
    if data.get('first_name'):
        user.first_name = data.get('first_name')
    if data.get('last_name'):
        user.last_name = data.get('last_name')
    if data.get('password'):
        user.password_hash = User.hash_password(data.get('password'))
    await session.flush()

    return web.json_response(UserResponse().dump(user))


@docs(
    tags=["Admin"],
    summary="Получение пользователя по его id",
    description="Получение пользователя по его id. Требуется аутентификация.",
    responses={
        200: {
            "schema": UserResponse,
            "description": "Пользователь успешно получен"
        },
        400: {
            "schema": ErrorResponse,
            "description": "передан id пользователя, которого не существует"
        },
        401: {
            "description": "Ошибка аутентификации (отсутствующий или неправильный токен аутентификации. "
                           "Authorization: Bearer 'текст токена') "
        },
    },
)
async def get_user_by_id(request: web.Request) -> web.Response:
    jwt_check(request)
    session = request['session']
    try:
        user = await User.get_by_id(session, request.match_info['id'])
        if not user:
            raise web.HTTPBadRequest(text="user with this id doesn't exists")
    except IntegrityError:
        raise web.HTTPBadRequest(text="user with this id doesn't exists")
    except DBAPIError:
        raise web.HTTPBadRequest(text="user with this id doesn't exists")
    return web.json_response(UserResponse().dump(user), status=200)
