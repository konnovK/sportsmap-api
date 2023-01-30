import logging
from functools import partial
from types import AsyncGeneratorType, MappingProxyType
from typing import AsyncIterable, Mapping

import aiohttp_cors
from aiohttp import web, PAYLOAD_REGISTRY
from aiohttp_apispec import setup_aiohttp_apispec

from api.handlers import ROUTES
from api.jwt import JWT
from api.middlewares import transaction_middleware, error_middleware
from settings import Settings
from api.payloads import AsyncGenJSONListPayload, JsonPayload
from utils import setup_db, setup_logger

logger = logging.getLogger(__name__)
setup_logger(logger)


def create_app(settings: Settings) -> web.Application:
    """
    Создает экземпляр приложения, готового к запуску.
    """
    app = web.Application(
        logger=logger,
    )
    app.middlewares.append(error_middleware)
    app.middlewares.append(transaction_middleware)

    app['jwt'] = JWT()

    app.cleanup_ctx.append(partial(setup_db, settings=settings))

    app.add_routes(ROUTES)

    # Автоматическая сериализация в json данных в HTTP ответах
    PAYLOAD_REGISTRY.register(AsyncGenJSONListPayload,
                              (AsyncGeneratorType, AsyncIterable))
    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping, MappingProxyType))

    # Автоматическая генерация swagger документации
    setup_aiohttp_apispec(
        app=app,
        title="SportsMap API",
        url="/swagger/swagger.json",
        swagger_path="/",
        static_path="/swagger"
    )

    # Настройка CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)

    return app
