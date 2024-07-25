from marshmallow import Schema, fields, post_load
from typing_extensions import Optional


class UserSchema(Schema):
    user_id = fields.Int(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True)
    created_at = fields.DateTime()
    role_id = fields.Int(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return UserModel(**data)


class UserModel:
    def __init__(self, username: str, email: str, password: str, role_id: int, user_id: Optional[int] = None,
                 created_at: Optional[str] = None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at
        self.role_id = role_id


class LoginRequestSchema(Schema):
    username = fields.Str()
    password = fields.Str()


class RegisterRequestSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)


class TokenResponseSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
