from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema
)
from sqlalchemy.exc import IntegrityError, DBAPIError

from db import Facility
from api.jwt import jwt_middleware
from api.schemas.error import ErrorResponse
from api.schemas.facility import (
    FacilityRequest,
    FacilityResponse,
    FacilityResponseList,
    SearchQuery
)


@docs(
    tags=["Facilities"],
    summary="Создание объекта",
    description="Создание нового спортивного объекта.",
    responses={
        201: {
            "schema": FacilityResponse,
            "description": "Спортивный объект успешно создан"
        },
        400: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации входных данных"
        },
        401: {
            "description": "Ошибка аутентификации (отсутствующий или неправильный токен аутентификации. "
                           "Authorization: Bearer 'текст токена') "
        },
    },
)
@request_schema(FacilityRequest)
@jwt_middleware
async def create_facility(request: web.Request) -> web.Response:
    data = FacilityRequest().load(await request.json())

    facility = Facility(**data)

    session = request.app['session']

    try:
        session.add(facility)
        await session.flush()
    except IntegrityError:
        raise web.HTTPConflict()
    except DBAPIError:
        raise web.HTTPBadRequest(text='bad enum value')

    return web.json_response(FacilityResponse().dump(facility), status=201)


@docs(
    tags=["Facilities"],
    summary="Обновление спортивного объекта",
    description="Обновление спортивного объекта.",
    responses={
        200: {
            "schema": FacilityResponse,
            "description": "Спортивный объект успешно обновлен"
        },
        400: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации входных данных"
        },
        401: {
            "description": "Ошибка аутентификации (отсутствующий или неправильный токен аутентификации. "
                           "Authorization: Bearer 'текст токена') "
        },
    },
)
@request_schema(FacilityRequest)
@jwt_middleware
async def update_facility(request: web.Request) -> web.Response:
    data = FacilityRequest().load(await request.json())

    facility_updated_fields = {}
    for k in data:
        if data.get(k) is not None:
            facility_updated_fields[k] = data.get(k)

    session = request.app['session']

    facility = await Facility.get_by_id(session, request.match_info['id'])

    for k in facility_updated_fields:
        setattr(facility, k, facility_updated_fields[k])

    await session.flush()

    return web.json_response(FacilityResponse().dump(facility), status=200)


@docs(
    tags=["Facilities"],
    summary="Удаление спортивного объекта",
    description="Удаление спортивного объекта.",
    responses={
        204: {
            "description": "Спортивный объект успешно удален"
        },
        400: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации входных данных"
        },
        401: {
            "description": "Ошибка аутентификации (отсутствующий или неправильный токен аутентификации. "
                           "Authorization: Bearer 'текст токена') "
        },
    },
)
@jwt_middleware
async def delete_facility(request: web.Request) -> web.Response:
    session = request.app['session']

    facility = await Facility.get_by_id(session, request.match_info['id'])
    await session.delete(facility)

    return web.json_response(status=204)


@docs(
    tags=["Facilities"],
    summary="Получение спортивного объекта по id",
    description="Получение спортивного объекта по id",
    responses={
        200: {
            "schema": FacilityResponse,
            "description": "Полученный объект"
        },
        400: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации входных данных"
        },
        401: {
            "description": "Ошибка аутентификации (отсутствующий или неправильный токен аутентификации. "
                           "Authorization: Bearer 'текст токена') "
        },
    },
)
@jwt_middleware
async def get_facility_by_id(request: web.Request) -> web.Response:
    session = request.app['session']
    try:
        facility = await Facility.get_by_id(session, request.match_info['id'])
        if not facility:
            raise web.HTTPBadRequest(text="facility with this id doesn't exists")
    except IntegrityError:
        raise web.HTTPBadRequest(text="facility with this id doesn't exists")
    except DBAPIError:
        raise web.HTTPBadRequest(text="facility with this id doesn't exists")
    return web.json_response(FacilityResponse().dump(facility), status=200)


@docs(
    tags=["Facilities"],
    summary="Получение всех спортивных объектов",
    description="Получение всех спортивных объектов",
    responses={
        200: {
            "schema": FacilityResponseList,
            "description": "Полученные объекты"
        },
        400: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации входных данных"
        },
        401: {
            "description": "Ошибка аутентификации (отсутствующий или неправильный токен аутентификации. "
                           "Authorization: Bearer 'текст токена') "
        },
    },
)
@jwt_middleware
async def get_all_facilities(request: web.Request) -> web.Response:
    session = request.app['session']

    facilities = await Facility.get_all(session)

    return web.json_response(FacilityResponseList().dump({
        'count': len(facilities),
        'data': [FacilityResponse().dump(facility) for facility in facilities]
    }), status=200)


@docs(
    tags=["Facilities"],
    summary="Поиск спортивных объектов",
    description="Типа очень умный поиск спортивных объектов, с фильтрами и прочей шнягой",
    responses={
        200: {
            "schema": FacilityResponseList,
            "description": "Полученные объекты"
        },
        400: {
            "schema": ErrorResponse,
            "description": "Ошибка валидации входных данных"
        },
        401: {
            "description": "Ошибка аутентификации (отсутствующий или неправильный токен аутентификации. "
                           "Authorization: Bearer 'текст токена') "
        },
    },
)
@request_schema(SearchQuery)
@jwt_middleware
async def search_facilities(request: web.Request) -> web.Response:
    data = SearchQuery().load(await request.json())

    session = request.app['session']

    q = data.get('q')
    limit = data.get('limit')
    offset = data.get('offset')
    order_by = data.get('order_by')
    order_desc = data.get('order_desc')
    filters = data.get('filters')

    facilities = await Facility.search(
        session,
        q=q,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
        filters=filters
    )

    return web.json_response(FacilityResponseList().dump({
        'count': len(facilities),
        'data': [FacilityResponse().dump(facility) for facility in facilities]
    }), status=200)
