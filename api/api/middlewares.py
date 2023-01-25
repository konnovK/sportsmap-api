import marshmallow
from aiohttp import web
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.error import ErrorResponse


@web.middleware
async def error_middleware(request: web.Request, handler):
    try:
        return await handler(request)
    except web.HTTPError as err:
        logger.debug(err)
        status_code = err.status_code
        return web.json_response(ErrorResponse().load({
            'message': err.text,
            'detail': {}
        }), status=status_code)
    except marshmallow.exceptions.ValidationError as err:
        logger.debug(f'validation error: {err}')
        status_code = 422
        return web.json_response(ErrorResponse().load({
            'message': 'validation error',
            'detail': err.messages
        }), status=status_code)
    except Exception as e:
        logger.exception(e)
        status_code = 500
        return web.json_response(ErrorResponse().load({
            'message': 'internal server error',
            'detail': {}
        }), status=status_code)


@web.middleware
async def transaction_middleware(request: web.Request, handler):
    async with request.app['sessionmaker']() as session:
        session: AsyncSession
        await session.begin()
        try:
            request['session'] = session
            resp = await handler(request)
            await session.commit()
            return resp
        except Exception:
            await session.rollback()
            raise
