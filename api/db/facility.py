from __future__ import annotations

import enum
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from .schema import Base


class FacilityTypes(enum.Enum):
    Flat = 'Flat'
    Gym = 'Gym'
    Pool = 'Pool'
    SkatingRink = 'SkatingRink'
    Shooting = 'Shooting'
    Other = 'Other'
    Outdoor = 'Outdoor'


class FacilityPropertyForms(enum.Enum):
    RussianFederationSubject = 'RussianFederationSubject'
    Federal = 'Federal'
    Municipal = 'Municipal'
    Private = 'Private'
    Other = 'Other'


class FacilityCoveringTypes(enum.Enum):
    Printed = 'Printed'
    RubberBitumen = 'RubberBitumen'
    RubberTile = 'RubberTile'
    Polymer = 'Polymer'
    Synthetic = 'Synthetic'


class FacilityPayingTypes(enum.Enum):
    FullFree = 'FullFree'
    PartlyFree = 'PartlyFree'
    NotFree = 'NotFree'


class Facility(Base):
    __tablename__ = 'facility'

    id = sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column('name', sa.String, nullable=False, unique=True)  # имя объекта
    x = sa.Column('x', sa.Float, nullable=False)  # КООРДИНАТА X
    y = sa.Column('y', sa.Float, nullable=False)  # КООРДИНАТА Y
    type = sa.Column('type', sa.Enum(FacilityTypes))  # тип объекта
    owner_name = sa.Column('owner_name', sa.String)  # ФИО владельца
    property_form = sa.Column('property_form', sa.Enum(FacilityPropertyForms))  # форма собственности
    length = sa.Column('length', sa.Float)  # длина
    width = sa.Column('width', sa.Float)  # ширина
    area = sa.Column('area', sa.Float)  # площадь
    actual_workload = sa.Column('actual_workload', sa.Integer)  # фактическая загруженность
    annual_capacity = sa.Column('annual_capacity', sa.Integer)  # годовая мощность
    notes = sa.Column('notes', sa.String)  # примечания
    height = sa.Column('height', sa.Float)  # высота
    size = sa.Column('size', sa.Float)  # размер
    depth = sa.Column('depth', sa.Float)  # глубина
    converting_type = sa.Column('converting_type', sa.Enum(FacilityCoveringTypes))  # типи покрытия
    is_accessible_for_disabled = sa.Column('is_accessible_for_disabled', sa.Boolean)  # доступность для инвалидов
    paying_type = sa.Column('paying_type', sa.Enum(FacilityPayingTypes))  # платные услуги
    who_can_use = sa.Column('who_can_use', sa.String)  # пользователь
    link = sa.Column('link', sa.String)  # ссылка на сайт
    phone_number = sa.Column('phone_number', sa.String)  # номер телефона
    open_hours = sa.Column('open_hours', sa.String)  # режим работы
    eps = sa.Column('eps', sa.Integer)  # ЕПС (что бы это ни было)
    hidden = sa.Column('hidden', sa.Boolean, default=False)  # видимость

    created_at = sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now())
    updated_at = sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())

    ix_id = sa.Index('ix__facility__id', id, postgresql_using='hash')
    ix_name = sa.Index('ix__facility__name', name, postgresql_using='hash')
    ix_x = sa.Index('ix__facility__x', x, postgresql_using='btree')
    ix_y = sa.Index('ix__facility__y', y, postgresql_using='btree')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')
        self.type = kwargs.get('type')
        self.owner_name = kwargs.get('owner_name')
        self.property_form = kwargs.get('property_form')
        self.length = kwargs.get('length')
        self.width = kwargs.get('width')
        self.area = kwargs.get('area')
        self.actual_workload = kwargs.get('actual_workload')
        self.annual_capacity = kwargs.get('annual_capacity')
        self.notes = kwargs.get('notes')
        self.height = kwargs.get('height')
        self.size = kwargs.get('size')
        self.depth = kwargs.get('depth')
        self.converting_type = kwargs.get('converting_type')
        self.is_accessible_for_disabled = kwargs.get('is_accessible_for_disabled')
        self.paying_type = kwargs.get('paying_type')
        self.who_can_use = kwargs.get('who_can_use')
        self.link = kwargs.get('link')
        self.phone_number = kwargs.get('phone_number')
        self.open_hours = kwargs.get('open_hours')
        self.eps = kwargs.get('eps')
        self.hidden = kwargs.get('hidden')

    def __repr__(self):
        return f'Facility(name={self.name} id={self.id} ({self.x};{self.y}))'

    def __str__(self):
        return f'Facility(name={self.name} id={self.id})'

    @staticmethod
    async def search(
            session: AsyncSession,
            q: str | None = None,
            limit: int | None = None,
            offset: int | None = None,
            order_by: str | None = None,
            order_desc: bool | None = None,
            filters: list[dict] | None = None
    ):
        stmt = sa.select(Facility)

        conditions = []
        for f in filters:
            cc = []
            field = f['field']
            eq = f.get('eq')
            lt = f.get('lt')
            gt = f.get('gt')
            if eq:
                cc.append(getattr(Facility, field) == eq)
            if lt:
                cc.append(getattr(Facility, field) <= lt)
            if gt:
                cc.append(getattr(Facility, field) >= gt)
            conditions.append(sa.and_(*cc))
        stmt = stmt.where(sa.or_(*conditions))
        # for c in conditions:
        #     stmt = stmt.where(c)

        if order_by:
            if order_desc:
                stmt = stmt.order_by(sa.desc(order_by))
            else:
                stmt = stmt.order_by(order_by)

        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)

        facilities = (await session.execute(stmt)).scalars().all()

        return facilities

    @staticmethod
    async def get_by_id(session: AsyncSession, id: str) -> Facility | None:
        facility = (
            await session.execute(
                sa.select(Facility)
                .where(Facility.id == id)
            )
        ).scalars().first()
        return facility

    @staticmethod
    async def get_all(session: AsyncSession) -> list[Facility]:
        facilities = (
            await session.execute(sa.select(Facility))
        ).scalars().all()
        return facilities

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "type": self.type,
            "owner_name": self.owner_name,
            "property_form": self.property_form,
            "length": self.length,
            "width": self.width,
            "area": self.area,
            "actual_workload": self.actual_workload,
            "annual_capacity": self.annual_capacity,
            "notes": self.notes,
            "height": self.height,
            "size": self.size,
            "depth": self.depth,
            "converting_type": self.converting_type,
            "is_accessible_for_disabled": self.is_accessible_for_disabled,
            "paying_type": self.paying_type,
            "who_can_use": self.who_can_use,
            "link": self.link,
            "phone_number": self.phone_number,
            "open_hours": self.open_hours,
            "eps": self.eps,
            "hidden": self.hidden,
        }
