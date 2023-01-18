from marshmallow import Schema, fields


class ErrorResponse(Schema):
    message = fields.String()
    detail = fields.Dict()
