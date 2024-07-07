from marshmallow import Schema, fields


class UserModel(Schema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True)  # Do not include password in the serialized output
    created_at = fields.DateTime(dump_only=True)
    role_id = fields.Int(required=True)


class LoginRequestSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class RegisterRequestSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)


class TokenResponseSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

