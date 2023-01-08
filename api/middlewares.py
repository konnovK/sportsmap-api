import marshmallow
from aiohttp import web
from loguru import logger

from api.schemas.error import ErrorResponse


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
