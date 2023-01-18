from marshmallow import Schema, fields


class FacilityRequest(Schema):
    name = fields.Str(required=True, nullable=False)  # имя объекта
    x = fields.Float(required=True, nullable=False)  # КООРДИНАТА X
    y = fields.Field(required=True, nullable=False)  # КООРДИНАТА Y
    type = fields.Str()  # тип объекта
    owner_name = fields.Str()  # ФИО владельца
    property_form = fields.Str()  # форма собственности
    length = fields.Field()  # длина
    width = fields.Field()  # ширина
    area = fields.Field()  # площадь
    actual_workload = fields.Int()  # фактическая загруженность
    annual_capacity = fields.Int()  # годовая мощность
    notes = fields.Str()  # примечания
    height = fields.Field()  # высота
    size = fields.Field()  # размер
    depth = fields.Field()  # глубина
    converting_type = fields.Str()  # типы покрытия
    is_accessible_for_disabled = fields.Bool()  # доступность для инвалидов
    paying_type = fields.Str(required=True, nullable=False)  # платные услуги
    who_can_use = fields.Str()  # пользователь
    link = fields.Str()  # ссылка на сайт
    phone_number = fields.Str()  # номер телефона
    open_hours = fields.Str()  # режим работы
    eps = fields.Int()  # ЕПС (что бы это ни было)
    hidden = fields.Bool()  # видимость


class FacilityResponse(Schema):
    id = fields.Str(required=True, nullable=False)
    name = fields.Str(required=True, nullable=False)  # имя объекта
    x = fields.Float(required=True, nullable=False)  # КООРДИНАТА X
    y = fields.Field(required=True, nullable=False)  # КООРДИНАТА Y
    type = fields.Str()  # тип объекта
    owner_name = fields.Str()  # ФИО владельца
    property_form = fields.Str()  # форма собственности
    length = fields.Field()  # длина
    width = fields.Field()  # ширина
    area = fields.Field()  # площадь
    actual_workload = fields.Int()  # фактическая загруженность
    annual_capacity = fields.Int()  # годовая мощность
    notes = fields.Str()  # примечания
    height = fields.Field()  # высота
    size = fields.Field()  # размер
    depth = fields.Field()  # глубина
    converting_type = fields.Str()  # типы покрытия
    is_accessible_for_disabled = fields.Bool()  # доступность для инвалидов
    paying_type = fields.Str(required=True, nullable=False)  # платные услуги
    who_can_use = fields.Str()  # пользователь
    link = fields.Str()  # ссылка на сайт
    phone_number = fields.Str()  # номер телефона
    open_hours = fields.Str()  # режим работы
    eps = fields.Int()  # ЕПС (что бы это ни было)
    hidden = fields.Bool()  # видимость
