from flask_restx import fields, Model, reqparse

from backend_server.v1.common.dto import Dto


class AccountDto:
    namespace = Dto.init('Account', path='/account', description='account related api')

    request_patch_user = reqparse.RequestParser()
    request_patch_user.add_argument('alias', type=str, location='args', default='')
    request_patch_user.add_argument('hours', type=int, location='args', help='time difference between local and utc')

    request_get_user = reqparse.RequestParser()
    request_get_user.add_argument('hours', type=int, location='args', help='time difference between local and utc')

    model_login: Model = namespace.model(
        'Account',
        {
            'username': fields.String(required=True, description='account name', example='admin'),
            'password': fields.String(required=True, description='account password', example='password')
        },
        mask="{*}"
    )

    model_user: Model = namespace.model(
        "User",
        {
            "username": fields.String(required=True, description='user name', example='admin'),
            "alias": fields.String(description='user alias'),
            "avatar": fields.String(description='user avatar'),
            "joined_date": fields.Integer(description='user joined time', attribute='created'),
            "update_date": fields.Integer(description='user info updated time', attribute='updated'),
        },
        mask="{*}"
    )

    model_resp: Model = Dto.set_resp(namespace, model_user)
