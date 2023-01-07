import time

import jwt
from jwt import DecodeError

JWT_SECRET = 'jwt_secret_tjli4k5ngiuhgze-hb8o65jh'


def create_jwt(email: str, jwt_secret: str = JWT_SECRET) -> (str, str, int):
    now = int(time.time())
    expires_in = now + 60 * 20  # + 20 minutes
    refresh_token = jwt.encode({
        'email': email,
    }, jwt_secret, algorithm="HS256")
    access_token = jwt.encode({
        'email': email,
        'refresh_token': refresh_token,
        'expires_in': expires_in
    }, jwt_secret, algorithm="HS256")
    return access_token, refresh_token, expires_in


def refresh_jwt(access_token: str, refresh_token: str, jwt_secret: str = JWT_SECRET) -> (str, str, int):
    access_token_data = jwt.decode(access_token, jwt_secret, algorithms=["HS256"])
    access_token_email = access_token_data['email']
    if access_token_data['refresh_token'] == refresh_token:
        return create_jwt(access_token_email, jwt_secret)
    else:
        return None, None, None


def check_access_token(access_token: str, jwt_secret: str = JWT_SECRET) -> bool:
    try:
        access_token_data = jwt.decode(access_token, jwt_secret, algorithms=["HS256"])
    except Exception:
        return False
    access_token_expires_in = access_token_data['expires_in']
    now = int(time.time())
    if now > access_token_expires_in:
        return False
    return True


def get_email_from_access_token(access_token: str, jwt_secret: str = JWT_SECRET) -> str | None:
    try:
        access_token_data = jwt.decode(access_token, jwt_secret, algorithms=["HS256"])
    except DecodeError:
        return None
    return access_token_data['email']
