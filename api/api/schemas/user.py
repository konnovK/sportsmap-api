from marshmallow import Schema, fields


class CreateUserRequest(Schema):
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email(required=True, nullable=False)
    password = fields.String(required=True, nullable=False)


class UserResponse(Schema):
    id = fields.UUID(required=True, nullable=False)
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email(required=True, nullable=False)


class LoginRequest(Schema):
    email = fields.Email(required=True, nullable=False)
    password = fields.String(required=True, nullable=False)


class LoginResponse(Schema):
    id = fields.UUID()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()
    group = fields.String()
    access_token = fields.String()
    access_token_expires_in = fields.Integer()
    refresh_token = fields.String()


class RefreshTokenRequest(Schema):
    access_token = fields.String(required=True, nullable=False)
    refresh_token = fields.String(required=True, nullable=False)


class UpdateSelfRequest(Schema):
    first_name = fields.String()
    last_name = fields.String()
    password = fields.String()
