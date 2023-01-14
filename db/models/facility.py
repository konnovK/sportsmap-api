from __future__ import annotations

import uuid
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa

from db.schema import facilities_table


@dataclass
class Facility:
    id: str | None
    name: str                                   # имя объекта
    x: float                                    # КООРДИНАТА X
    y: float                                    # КООРДИНАТА Y
    type: str                                   # тип объекта
    owner_name: str | None                      # ФИО владельца
    property_form: str                          # форма собственности
    length: float | None                        # длина
    width: float | None                         # ширина
    area: float | None                          # площадь
    actual_workload: int | None                 # фактическая загруженность
    annual_capacity: int | None                 # годовая мощность
    notes: str | None                           # примечания
    height: float | None                        # высота
    size: float | None                          # размер
    depth: float | None                         # глубина
    converting_type: str | None                 # типи покрытия
    is_accessible_for_disabled: bool | None     # доступность для инвалидов
    paying_type: str                            # платные услуги
    who_can_use: str | None                     # пользователь
    link: str | None                            # ссылка на сайт
    phone_number: str | None                    # номер телефона
    open_hours: str | None                      # режим работы
    eps: int | None                             # ЕПС (что бы это ни было)
    hidden: bool | None                         # видимость

    def dict(self) -> dict:
        result = {
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'type': self.type,
        }
        if self.owner_name:
            result['owner_name'] = self.owner_name
        if self.property_form:
            result['property_form'] = self.property_form
        if self.length:
            result['length'] = self.length
        if self.width:
            result['width'] = self.width
        if self.area:
            result['area'] = self.area
        if self.actual_workload:
            result['actual_workload'] = self.actual_workload
        if self.annual_capacity:
            result['annual_capacity'] = self.annual_capacity
        if self.notes:
            result['notes'] = self.notes
        if self.height:
            result['height'] = self.height
        if self.size:
            result['size'] = self.size
        if self.depth:
            result['depth'] = self.depth
        if self.converting_type:
            result['converting_type'] = self.converting_type
        if self.is_accessible_for_disabled:
            result['is_accessible_for_disabled'] = self.is_accessible_for_disabled
        if self.paying_type:
            result['paying_type'] = self.paying_type
        if self.who_can_use:
            result['who_can_use'] = self.who_can_use
        if self.link:
            result['link'] = self.link
        if self.phone_number:
            result['phone_number'] = self.phone_number
        if self.open_hours:
            result['open_hours'] = self.open_hours
        if self.eps:
            result['eps'] = self.eps
        if self.hidden:
            result['hidden'] = self.hidden

        return result

    @staticmethod
    def from_dict(facility: dict) -> Facility:
        return Facility(
            id=facility.get('id'),
            name=facility.get('name'),
            x=facility.get('x'),
            y=facility.get('y'),
            type=facility.get('type'),
            owner_name=facility.get('owner_name'),
            property_form=facility.get('property_form'),
            length=facility.get('length'),
            width=facility.get('width'),
            area=facility.get('area'),
            actual_workload=facility.get('actual_workload'),
            annual_capacity=facility.get('annual_capacity'),
            notes=facility.get('notes'),
            height=facility.get('height'),
            size=facility.get('size'),
            depth=facility.get('depth'),
            converting_type=facility.get('converting_type'),
            is_accessible_for_disabled=facility.get('is_accessible_for_disabled'),
            paying_type=facility.get('paying_type'),
            who_can_use=facility.get('who_can_use'),
            link=facility.get('link'),
            phone_number=facility.get('phone_number'),
            open_hours=facility.get('open_hours'),
            eps=facility.get('eps'),
            hidden=facility.get('hidden'),
        )

    def __repr__(self):
        return f'<Facility {self.name} ({self.x}, {self.y}) {self.id}>'

    def __str__(self):
        return f'<Facility {self.name} ({self.x}, {self.y}) {self.id}>'

    @staticmethod
    async def create(conn: AsyncConnection, facility: dict) -> str:
        """
        Создает в БД объект.

        :param conn: соединение с БД
        :param facility: словарь с полями объекта, которые мы хотим создать
        :returns: id созданного объекта
        """
        facility = Facility.from_dict(facility).dict()
        if 'id' in facility:
            del facility['id']

        facility_id = str(uuid.uuid4())
        await conn.execute(
            sa.insert(facilities_table).values(
                id=facility_id,
                **facility
            )
        )
        return facility_id

    @staticmethod
    async def exists(conn: AsyncConnection, facility_name: str) -> bool:
        """
        Проверяет, существует ли объект

        :param conn: соединение с БД
        :param facility_name: название объекта
        :returns: существует ли объект
        """
        selected_facility = (await conn.execute(
            sa.select(facilities_table).where(facilities_table.c.name == facility_name)
        )).first()
        if selected_facility:
            return True
        return False

    @staticmethod
    async def delete(conn: AsyncConnection, facility_id: str):
        """
        Удаляет объект по его id
        """
        await conn.execute(sa.delete(facilities_table).where(facilities_table.c.id == facility_id))

    @staticmethod
    async def update(conn: AsyncConnection, facility_id: str, facility: dict) -> Facility:
        """
        Изменяет в БД объект.

        :param conn: соединение с БД
        :param facility_id: id объекта
        :param facility: словарь с полями объекта, которые мы хотим поменять
        :returns: id созданного объекта
        """
        facility = Facility.from_dict(facility).dict()
        if 'id' in facility:
            del facility['id']

        updated_facility_id = (await conn.execute(
            sa.update(facilities_table).where(facilities_table.c.id == facility_id).values(**facility).returning(
                facilities_table.c.id
            )
        )).first()

        return await Facility.get_by_id(conn, updated_facility_id)

    @staticmethod
    async def get_by_id(conn: AsyncConnection, facility_id: str) -> Facility:
        """
        Получение объекта по его id

        :param conn: соединение с БД
        :param facility_id: id объекта
        :returns: полученный объект
        """
        selected_facility = (await conn.execute(
            sa.select(facilities_table).where(facilities_table.c.id == facility_id)
        )).first()
        return Facility(
            id=selected_facility.id,
            name=selected_facility.name,
            x=selected_facility.x,
            y=selected_facility.y,
            type=selected_facility.type,
            owner_name=selected_facility.owner_name,
            property_form=selected_facility.property_form,
            length=selected_facility.length,
            width=selected_facility.width,
            area=selected_facility.area,
            actual_workload=selected_facility.actual_workload,
            annual_capacity=selected_facility.annual_capacity,
            notes=selected_facility.notes,
            height=selected_facility.height,
            size=selected_facility.size,
            depth=selected_facility.depth,
            converting_type=selected_facility.converting_type,
            is_accessible_for_disabled=selected_facility.is_accessible_for_disabled,
            paying_type=selected_facility.paying_type,
            who_can_use=selected_facility.who_can_use,
            link=selected_facility.link,
            phone_number=selected_facility.phone_number,
            open_hours=selected_facility.open_hours,
            eps=selected_facility.eps,
            hidden=selected_facility.hidden,
        )
