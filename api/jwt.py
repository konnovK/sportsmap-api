import random
import time

from aiohttp import web
import jwt
from jwt import PyJWTError
from loguru import logger

class JWTException(Exception):
    """
    Исключение, которое выбрасивают методы, работающие с jwt.
    """
    pass


class JWT:
    """
    Класс для работы с jwt токенами.
    """
    def __init__(self):
        self.JWT_SECRET = ''.join(random.choice('qwertyuiopasdfghjklzxcvbnm123456789') for _ in range(128))
        self.TOKEN_TTL_SECONDS = 60 * 20

    def __encode_jwt(self, data: dict) -> str:
        try:
            jwt_secret = self.JWT_SECRET
            return jwt.encode(data, jwt_secret, algorithm="HS256")
        except PyJWTError:
            raise JWTException

    def __decode_jwt(self, token: str) -> dict:
        try:
            jwt_secret = self.JWT_SECRET
            return jwt.decode(token, jwt_secret, algorithms=["HS256"])
        except PyJWTError:
            raise JWTException

    def create_jwt(self, email: str) -> (str, str, int):
        """
        Создает access token и refresh token.
        :raise JWTException: если случилась ошибка при создании токенов
        :param email: email аутентифицируемого пользователя
        :return: тройка (access_token, refresh_token, expires_in)
        """
        now = int(time.time())
        expires_in = now + self.TOKEN_TTL_SECONDS
        access_token = self.__encode_jwt({
            'email': email,
            'created_in': now,
            'expires_in': expires_in
        })
        refresh_token = self.__encode_jwt({
            'email': email,
            'created_in': now,
            'access_token': access_token
        })
        return access_token, refresh_token, expires_in

    def refresh_jwt(self, access_token: str, refresh_token: str) -> (str, str, int):
        """
        Обновляет access token и refresh token.
        :raise JWTException: если токены некорректные
        :param access_token: access token
        :param refresh_token: refresh token
        :return: тройка (access_token, refresh_token, expires_in)
        """
        access_token_data = self.__decode_jwt(access_token)
        refresh_token_data = self.__decode_jwt(refresh_token)
        try:
            refresh_token_decoded_access_token = refresh_token_data['access_token']
            refresh_token_created_in = refresh_token_data['created_in']
            access_token_created_in = access_token_data['created_in']
            refresh_token_email = refresh_token_data['email']
            access_token_email = access_token_data['email']
        except ValueError:
            raise JWTException
        if (
                refresh_token_decoded_access_token == access_token and
                refresh_token_created_in == access_token_created_in and
                refresh_token_email == access_token_email
        ):
            return self.create_jwt(access_token_email)
        else:
            raise JWTException

    def check_access_token(self, access_token: str) -> bool:
        """
        Проверяет, жив ли еще токен.
        :raise JWTException: если токен некорректный
        :param access_token: токен
        :return: True - если токен еще жив, False - иначе
        """
        access_token_data = self.__decode_jwt(access_token)
        try:
            access_token_expires_in = access_token_data['expires_in']
        except ValueError:
            raise JWTException
        now = int(time.time())
        if now > access_token_expires_in:
            return False
        return True

    def get_email_from_access_token(self, access_token: str) -> str:
        access_token_data = self.__decode_jwt(access_token)
        try:
            access_token_email = access_token_data['email']
        except ValueError:
            raise JWTException
        return access_token_email


def jwt_middleware(handler):
    """
    Собственный промежуточный обработчик (декоратор) для проверки jwt токена.

    После проверки токена в request.app['user'] будет находиться объект аутентифицированного пользователя
    """
    async def wrapper(request: web.Request):
        logger.debug('JWT Check')
        logger.debug(request.url.path)
        logger.debug(f"HEADER: Authorization: {request.headers.get('Authorization')}")
        if not request.headers.get('Authorization'):
            raise web.HTTPUnauthorized()
        if request.headers.get('Authorization').split(' ')[0] != 'Bearer':
            raise web.HTTPUnauthorized()
        try:
            access_token = request.headers.get('Authorization').split(' ')[1]
        except KeyError:
            raise web.HTTPUnauthorized()
        try:
            check_access_token = request.app['jwt'].check_access_token(access_token)
        except JWTException:
            raise web.HTTPUnauthorized()
        if not check_access_token:
            raise web.HTTPUnauthorized()
        try:
            user_email = request.app['jwt'].get_email_from_access_token(access_token)
        except JWTException:
            raise web.HTTPUnauthorized()

        request.app['email'] = user_email
        response = await handler(request)
        return response
    return wrapper
