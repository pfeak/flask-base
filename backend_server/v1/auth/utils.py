from marshmallow import Schema, fields, pre_load, post_load, validates, ValidationError, pre_dump, post_dump, EXCLUDE
from marshmallow.validate import Length, Regexp

from backend_server.models.common import TimeUtils
from backend_server.models.user import UserModel


class LoginSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    username = fields.String(
        required=True,
        validate=[Length(min=4, max=15),
                  Regexp(
                      r"[a-z]",
                      error="Invalid username! username must be [a-z]",
                  )])
    password_hash = fields.String(load_only=True, data_key='password', missing=None)
    token = fields.String(dump_only=True, missing=None)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)

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
        data['created'] = TimeUtils.utc2local(data['created'], self.hours)
        data['updated'] = TimeUtils.utc2local(data['updated'], self.hours)
        return data
