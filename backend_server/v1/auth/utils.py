from marshmallow import Schema, fields, pre_load, post_load, pre_dump, post_dump, EXCLUDE
from marshmallow.validate import Length, Regexp

from backend_server.common.base import TimeUtils
from backend_server.models.user import UserModel


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(
        required=False,
        validate=[Length(min=4, max=15),
                  Regexp(
                      r"[a-z]",
                      error="Invalid username! username must be [a-z]",
                  )])
    password_hash = fields.String(load_only=True, data_key='password', missing=None)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)


class LoginSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user = fields.Nested(UserSchema)
    access_token = fields.String(missing=None)
    refresh_token = fields.String(missing=None)

    def __init__(self, hours: int = 8):
        super(LoginSchema, self).__init__()
        self.hours = hours

    @pre_load
    def pre_from_data(self, data, **kwargs):
        return data

    @post_load
    def from_data(self, data, **kwargs):
        return UserModel(**data)

    @pre_dump
    def pre_to_data(self, data, **kwargs):
        return data

    @post_dump
    def to_data(self, data, **kwargs):
        data['user']['created'] = TimeUtils.utc2local(data['user']['created'], self.hours)
        data['user']['updated'] = TimeUtils.utc2local(data['user']['updated'], self.hours)
        return data
