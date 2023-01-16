from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

import sqlalchemy as sa

from db.data.mapper import Mapper
from db.data.record import Record
from db.schema import facilities_table


@dataclass
class Facility(Record):
    id: str | None
    name: str  # имя объекта
    x: float  # КООРДИНАТА X
    y: float  # КООРДИНАТА Y
    type: str  # тип объекта
    owner_name: str | None  # ФИО владельца
    property_form: str  # форма собственности
    length: float | None  # длина
    width: float | None  # ширина
    area: float | None  # площадь
    actual_workload: int | None  # фактическая загруженность
    annual_capacity: int | None  # годовая мощность
    notes: str | None  # примечания
    height: float | None  # высота
    size: float | None  # размер
    depth: float | None  # глубина
    converting_type: str | None  # типи покрытия
    is_accessible_for_disabled: bool | None  # доступность для инвалидов
    paying_type: str  # платные услуги
    who_can_use: str | None  # пользователь
    link: str | None  # ссылка на сайт
    phone_number: str | None  # номер телефона
    open_hours: str | None  # режим работы
    eps: int | None  # ЕПС (что бы это ни было)
    hidden: bool | None  # видимость

    def __repr__(self):
        return f'Facility(name={self.name})'

    def __str__(self):
        return f'Facility(name={self.name})'

    def dict(self) -> dict[str, Any]:
        result = {}

        if self.id is not None:
            result['id'] = self.id
        if self.name is not None:
            result['name'] = self.name
        if self.x is not None:
            result['x'] = self.x
        if self.y is not None:
            result['y'] = self.y
        if self.type is not None:
            result['type'] = self.type
        if self.owner_name is not None:
            result['owner_name'] = self.owner_name
        if self.property_form is not None:
            result['property_form'] = self.property_form
        if self.length is not None:
            result['length'] = self.length
        if self.width is not None:
            result['width'] = self.width
        if self.area is not None:
            result['area'] = self.area
        if self.actual_workload is not None:
            result['actual_workload'] = self.actual_workload
        if self.annual_capacity is not None:
            result['annual_capacity'] = self.annual_capacity
        if self.notes is not None:
            result['notes'] = self.notes
        if self.height is not None:
            result['height'] = self.height
        if self.size is not None:
            result['size'] = self.size
        if self.depth is not None:
            result['depth'] = self.depth
        if self.converting_type is not None:
            result['converting_type'] = self.converting_type
        if self.is_accessible_for_disabled is not None:
            result['is_accessible_for_disabled'] = self.is_accessible_for_disabled
        if self.paying_type is not None:
            result['paying_type'] = self.paying_type
        if self.who_can_use is not None:
            result['who_can_use'] = self.who_can_use
        if self.link is not None:
            result['link'] = self.link
        if self.phone_number is not None:
            result['phone_number'] = self.phone_number
        if self.open_hours is not None:
            result['open_hours'] = self.open_hours
        if self.eps is not None:
            result['eps'] = self.eps
        if self.hidden is not None:
            result['hidden'] = self.hidden

        return result

    @staticmethod
    def from_dict(as_dict) -> Facility:
        return Facility(
            id=as_dict.get('id'),
            name=as_dict.get('name'),
            x=as_dict.get('x'),
            y=as_dict.get('y'),
            type=as_dict.get('type'),
            owner_name=as_dict.get('owner_name'),
            property_form=as_dict.get('property_form'),
            length=as_dict.get('length'),
            width=as_dict.get('width'),
            area=as_dict.get('area'),
            actual_workload=as_dict.get('actual_workload'),
            annual_capacity=as_dict.get('annual_capacity'),
            notes=as_dict.get('notes'),
            height=as_dict.get('height'),
            size=as_dict.get('size'),
            depth=as_dict.get('depth'),
            converting_type=as_dict.get('converting_type'),
            is_accessible_for_disabled=as_dict.get('is_accessible_for_disabled'),
            paying_type=as_dict.get('paying_type'),
            who_can_use=as_dict.get('who_can_use'),
            link=as_dict.get('link'),
            phone_number=as_dict.get('phone_number'),
            open_hours=as_dict.get('open_hours'),
            eps=as_dict.get('eps'),
            hidden=as_dict.get('hidden'),
        )

    @staticmethod
    def new(**kwargs) -> Facility:
        kwargs['id'] = str(uuid.uuid4())
        return Facility.from_dict(kwargs)


class FacilityMapper(Mapper):
    async def save(self, facility: Facility) -> Any | None:
        """
        Сохраняет объект в БД. Если его там не было, то он создается, если он там был, то обновляется.

        Возвращает id объекта, если он был добавлен в БД, или None, если он был обновлен в БД
        """
        select_id_stmt = sa.select(facilities_table.c.id).where(facilities_table.c.id == facility.id)
        selected_facility = await self._execute_then_first(select_id_stmt)
        if not selected_facility:
            insert_facility_stmt = sa.insert(facilities_table)\
                .values(**facility.dict())\
                .returning(facilities_table.c.id)
            inserted_facility = await self._execute_then_first(insert_facility_stmt)
            return inserted_facility._mapping['id']
        else:
            update_facility_stmt = sa.update(facilities_table)\
                .where(facilities_table.c.id == facility.id).values(**facility.dict())
            await self._execute(update_facility_stmt)
            return None

    async def delete(self, facility: Facility) -> None:
        """
        Удаляет пользователя из БД
        """
        stmt = sa.delete(facilities_table).where(facilities_table.c.id == facility.id)
        await self._execute(stmt)

    async def get_by_id(self, id: str) -> Facility | None:
        stmt = sa.select(facilities_table).where(facilities_table.c.id == id)
        facility = await self._execute_then_first(stmt)
        if facility is None:
            return None
        return Facility.from_dict(facility._mapping)
