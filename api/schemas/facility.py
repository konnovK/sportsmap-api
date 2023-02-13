from marshmallow import Schema, fields

from db.facility import FacilityTypes, FacilityPayingTypes, FacilityCoveringTypes, FacilityPropertyForms


class FacilityRequest(Schema):
    name = fields.Str(required=True, nullable=False)  # имя объекта
    x = fields.Float(required=True, nullable=False)  # КООРДИНАТА X
    y = fields.Float(required=True, nullable=False)  # КООРДИНАТА Y
    type = fields.Enum(FacilityTypes)  # тип объекта
    owner_name = fields.Str()  # ФИО владельца
    property_form = fields.Enum(FacilityPropertyForms)  # форма собственности
    length = fields.Float()  # длина
    width = fields.Float()  # ширина
    area = fields.Float()  # площадь
    actual_workload = fields.Int()  # фактическая загруженность
    annual_capacity = fields.Int()  # годовая мощность
    notes = fields.Str()  # примечания
    height = fields.Float()  # высота
    size = fields.Float()  # размер
    depth = fields.Float()  # глубина
    converting_type = fields.Enum(FacilityCoveringTypes)  # типы покрытия
    is_accessible_for_disabled = fields.Bool()  # доступность для инвалидов
    paying_type = fields.Enum(FacilityPayingTypes)  # платные услуги
    who_can_use = fields.Str()  # пользователь
    link = fields.Str()  # ссылка на сайт
    phone_number = fields.Str()  # номер телефона
    open_hours = fields.Str()  # режим работы
    eps = fields.Int()  # ЕПС (что бы это ни было)
    hidden = fields.Bool()  # видимость


class FacilityUpdateRequest(Schema):
    name = fields.Str()  # имя объекта
    x = fields.Float()  # КООРДИНАТА X
    y = fields.Float()  # КООРДИНАТА Y
    type = fields.Enum(FacilityTypes)  # тип объекта
    owner_name = fields.Str()  # ФИО владельца
    property_form = fields.Enum(FacilityPropertyForms)  # форма собственности
    length = fields.Float()  # длина
    width = fields.Float()  # ширина
    area = fields.Float()  # площадь
    actual_workload = fields.Int()  # фактическая загруженность
    annual_capacity = fields.Int()  # годовая мощность
    notes = fields.Str()  # примечания
    height = fields.Float()  # высота
    size = fields.Float()  # размер
    depth = fields.Float()  # глубина
    converting_type = fields.Enum(FacilityCoveringTypes)  # типы покрытия
    is_accessible_for_disabled = fields.Bool()  # доступность для инвалидов
    paying_type = fields.Enum(FacilityPayingTypes)  # платные услуги
    who_can_use = fields.Str()  # пользователь
    link = fields.Str()  # ссылка на сайт
    phone_number = fields.Str()  # номер телефона
    open_hours = fields.Str()  # режим работы
    eps = fields.Int()  # ЕПС (что бы это ни было)
    hidden = fields.Bool()  # видимость


class FacilityResponse(Schema):
    id = fields.UUID(required=True, nullable=False)
    name = fields.Str(required=True, nullable=False)  # имя объекта
    x = fields.Float(required=True, nullable=False)  # КООРДИНАТА X
    y = fields.Float(required=True, nullable=False)  # КООРДИНАТА Y
    type = fields.Str()  # тип объекта
    owner_name = fields.Str()  # ФИО владельца
    property_form = fields.Str()  # форма собственности
    length = fields.Float()  # длина
    width = fields.Float()  # ширина
    area = fields.Float()  # площадь
    actual_workload = fields.Int()  # фактическая загруженность
    annual_capacity = fields.Int()  # годовая мощность
    notes = fields.Str()  # примечания
    height = fields.Float()  # высота
    size = fields.Float()  # размер
    depth = fields.Float()  # глубина
    converting_type = fields.Str()  # типы покрытия
    is_accessible_for_disabled = fields.Bool()  # доступность для инвалидов
    paying_type = fields.Str()  # платные услуги
    who_can_use = fields.Str()  # пользователь
    link = fields.Str()  # ссылка на сайт
    phone_number = fields.Str()  # номер телефона
    open_hours = fields.Str()  # режим работы
    eps = fields.Int()  # ЕПС (что бы это ни было)
    hidden = fields.Bool()  # видимость


class FacilityResponseList(Schema):
    count = fields.Int(required=True, nullable=False)
    data = fields.List(fields.Nested(FacilityResponse()), required=True, nullable=False)


class FieldFilter(Schema):
    field = fields.Str()
    eq = fields.Str()
    lt = fields.Number()
    gt = fields.Number()


class SearchQuery(Schema):
    q = fields.Str()
    limit = fields.Int()
    offset = fields.Int()
    order_by = fields.Str()
    order_desc = fields.Bool()

    filters = fields.List(fields.Nested(FieldFilter()))


class FacilityPatchRequest(Schema):
    name = fields.Str()  # имя объекта
    x = fields.Float()  # КООРДИНАТА X
    y = fields.Float()  # КООРДИНАТА Y
    type = fields.Enum(FacilityTypes)  # тип объекта
    owner_name = fields.Str()  # ФИО владельца
    property_form = fields.Enum(FacilityPropertyForms)  # форма собственности
    length = fields.Float()  # длина
    width = fields.Float()  # ширина
    area = fields.Float()  # площадь
    actual_workload = fields.Int()  # фактическая загруженность
    annual_capacity = fields.Int()  # годовая мощность
    notes = fields.Str()  # примечания
    height = fields.Float()  # высота
    size = fields.Float()  # размер
    depth = fields.Float()  # глубина
    converting_type = fields.Enum(FacilityCoveringTypes)  # типы покрытия
    is_accessible_for_disabled = fields.Bool()  # доступность для инвалидов
    paying_type = fields.Enum(FacilityPayingTypes)  # платные услуги
    who_can_use = fields.Str()  # пользователь
    link = fields.Str()  # ссылка на сайт
    phone_number = fields.Str()  # номер телефона
    open_hours = fields.Str()  # режим работы
    eps = fields.Int()  # ЕПС (что бы это ни было)
    hidden = fields.Bool()  # видимость
