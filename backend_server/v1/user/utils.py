from marshmallow import Schema, fields, pre_load, post_load, validates, ValidationError, pre_dump, post_dump
from marshmallow.validate import Length, Regexp

from backend_server.models.common import TimeUtils
from backend_server.models.user import UserModel


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(
        required=True,
        validate=[Length(min=4, max=15),
                  Regexp(
                      r"[a-z]",
                      error="Invalid username! username must be [a-z]",
                  )])
    password_hash = fields.String(load_only=True, data_key='password', missing=None)
    alias = fields.String(missing=None)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)

    def __init__(self, hours: int = 8):
        super(UserSchema, self).__init__()
        self.hours = hours

    @validates("alias")
    def validate_alias(self, value):
        length = len(value)
        if length < 4:
            raise ValidationError("alias must be greater than 4.")
        if length > 10:
            raise ValidationError("alias must not be greater than 10.")

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
