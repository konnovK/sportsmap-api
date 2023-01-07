import marshmallow
from aiohttp import web
from loguru import logger

from api.jwt import get_email_from_access_token, check_access_token
from api.schemas.error import ErrorResponse


@web.middleware
async def jwt_middleware(request: web.Request, handler):
    logger.debug(f'JWT Check')
    logger.debug(request.url.path)
    logger.debug(f"HEADER: Authorization: {request.headers.get('Authorization')}")
    if (
            request.url.path.startswith('/api/docs') or
            request.url.path.startswith('/static/swagger') or
            request.url.path == '/' or
            request.url.path == '/ping' or
            (request.url.path == '/api/admin/users' and request.method == 'POST') or
            request.url.path == '/api/admin/login' or
            request.url.path == '/api/admin/token/refresh' or
            request.method == 'GET'  # TODO: Но это не точно
    ):
        logger.debug(f'JWT Passed')
        return await handler(request)
    if not request.headers.get('Authorization'):
        raise web.HTTPUnauthorized()
    try:
        access_token = request.headers.get('Authorization').split(' ')[1]
    except KeyError:
        raise web.HTTPUnauthorized()
    if not check_access_token(access_token):
        raise web.HTTPUnauthorized()
    user_email = get_email_from_access_token(access_token)
    request.app['email'] = user_email
    logger.debug(f'JWT Ok, email = {user_email}')
    response = await handler(request)
    return response


@web.middleware
async def error_middleware(request: web.Request, handler):
    try:
        return await handler(request)
    except web.HTTPUnauthorized as err:
        logger.debug(err)
        raise err
    except web.HTTPException as err:
        # Исключения которые представляют из себя HTTP ответ, были брошены
        # осознанно для отображения клиенту.
        logger.debug(err)
        raise web.HTTPBadRequest(body=ErrorResponse().load({
            'message': err.text,
            'detail': {}
        }))
        # raise web.HTTPBadRequest(body={'error': err.text}, content_type='application/json')
    except marshmallow.exceptions.ValidationError as err:
        logger.debug(f'validation error: {err}')
        raise web.HTTPBadRequest(body=ErrorResponse().load({
            'message': 'validation error',
            'detail': err.messages
        }))
    except Exception as e:
        # Исключения, которые бросили не мы
        logger.exception(e)
        raise e
