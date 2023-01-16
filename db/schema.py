import enum

import sqlalchemy as sa

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


"""
Таблица пользователей
"""
users_table = sa.Table(
    'users',
    metadata,
    sa.Column('id', sa.String, primary_key=True, nullable=False),
    sa.Column('first_name', sa.String),
    sa.Column('last_name', sa.String),
    sa.Column('email', sa.String, nullable=False, unique=True),
    sa.Column('password_hash', sa.String, nullable=False),
)

"""
Таблица адресов для почтовых рассылок
"""
mailings_table = sa.Table(
    'mailings',
    metadata,
    sa.Column('id', sa.String, primary_key=True, nullable=False),
    sa.Column('email', sa.String, nullable=False, unique=True),
)

"""
Таблица отзывов, оставленных на сайте через специальное поле
"""
feedbacks_table = sa.Table(
    'feedbacks',
    metadata,
    sa.Column('id', sa.String, primary_key=True, nullable=False),
    sa.Column('full_name', sa.String),
    sa.Column('contacts', sa.String),
    sa.Column('feedback', sa.String),
)


class FacilityTypes(enum.Enum):
    Flat = 'Flat'
    Gym = 'Gym'
    Pool = 'Pool'
    SkatingRink = 'SkatingRink'
    Shooting = 'Shooting'
    Other = 'Other'
    Outdoor = 'Outdoor'


class FacilityPropertyForms(enum.Enum):
    Unknown = 'Unknown'
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


"""
Таблица спортивных объектов
"""
facilities_table = sa.Table(
    'facilities',
    metadata,
    sa.Column('id', sa.String, primary_key=True, nullable=False),
    sa.Column('type', sa.Enum(FacilityTypes), nullable=False),  # тип объекта
    sa.Column('name', sa.String, nullable=False, unique=True),  # имя объекта
    sa.Column('x', sa.Float, nullable=False),  # КООРДИНАТА X
    sa.Column('y', sa.Float, nullable=False),  # КООРДИНАТА Y
    sa.Column('owner_name', sa.String),  # ФИО владельца
    sa.Column('property_form', sa.Enum(FacilityPropertyForms), nullable=False),  # форма собственности
    sa.Column('length', sa.Float),  # длина
    sa.Column('width', sa.Float),  # ширина
    sa.Column('area', sa.Float),  # площадь
    sa.Column('actual_workload', sa.Integer),  # фактическая загруженность
    sa.Column('annual_capacity', sa.Integer),  # годовая мощность
    sa.Column('notes', sa.String),  # примечания
    sa.Column('height', sa.Float),  # высота
    sa.Column('size', sa.Float),  # размер
    sa.Column('depth', sa.Float),  # глубина
    sa.Column('converting_type', sa.Enum(FacilityCoveringTypes)),  # типи покрытия
    sa.Column('is_accessible_for_disabled', sa.Boolean),  # доступность для инвалидов
    sa.Column('paying_type', sa.Enum(FacilityPayingTypes), nullable=False),  # платные услуги
    sa.Column('who_can_use', sa.String),  # пользователь
    sa.Column('link', sa.String),  # ссылка на сайт
    sa.Column('phone_number', sa.String),  # номер телефона
    sa.Column('open_hours', sa.String),  # режим работы
    sa.Column('eps', sa.Integer),  # ЕПС (что бы это ни было)
    sa.Column('hidden', sa.Boolean, nullable=False),  # видимость
)
