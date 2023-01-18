from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
)

from api.jwt import jwt_middleware
from api.schemas.error import ErrorResponse
from api.schemas.facility import FacilityRequest, FacilityResponse
from db.data.facility import Facility, FacilityMapper


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
    facility = Facility.new(**data)

    async with request.app['db'].begin() as conn:
        facility_mapper = FacilityMapper(conn)

        if await facility_mapper.get_by_name(facility.name):
            return web.json_response(status=409)
        await facility_mapper.save(facility)

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

    async with request.app['db'].begin() as conn:
        facility_mapper = FacilityMapper(conn)

        facility = await facility_mapper.get_by_id(request.match_info['id'])
        if facility is None:
            return web.HTTPBadRequest(text="facility with this id doesn't exists")

        facility = Facility.from_dict({
            **facility.dict(),
            **facility_updated_fields
        })
        await facility_mapper.save(facility)

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
    async with request.app['db'].begin() as conn:
        facility_mapper = FacilityMapper(conn)

        facility = await facility_mapper.get_by_id(request.match_info['id'])
        if facility is None:
            return web.HTTPBadRequest(text="facility with this id doesn't exists")

        await facility_mapper.delete(facility)

    return web.json_response(status=204)
