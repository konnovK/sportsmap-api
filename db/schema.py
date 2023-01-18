import enum
import uuid

import sqlalchemy as sa
from sqlalchemy.orm import as_declarative

from utils import hash_password

# SQLAlchemy рекомендует использовать единый формат для генерации названий для
# индексов и внешних ключей.
# https://docs.sqlalchemy.org/en/13/core/constraints.html#configuring-constraint-naming-conventions
convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = sa.MetaData(naming_convention=convention)


@as_declarative(metadata=metadata)
class Base:
    pass


class User(Base):
    __tablename__ = 'user'

    id = sa.Column('id', sa.String, primary_key=True, nullable=False)
    first_name = sa.Column('first_name', sa.String)
    last_name = sa.Column('last_name', sa.String)
    email = sa.Column('email', sa.String, nullable=False, unique=True)
    password_hash = sa.Column('password_hash', sa.String, nullable=False)

    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.email = kwargs.get('email')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.password_hash = hash_password(kwargs.get('password'))

    def check_password(self, password: str):
        return self.password_hash == hash_password(password)


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

    id = sa.Column('id', sa.String, primary_key=True, nullable=False)
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

    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
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
