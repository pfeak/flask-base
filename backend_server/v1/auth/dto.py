from flask_restx import Model, fields

from backend_server.v1.common.dto import Dto


class AuthDto:
    namespace = Dto.init('auth', path='/auth', description='auth related api')

    model_login: Model = namespace.model(
        'Auth-model',
        {
            'username': fields.String(required=True, description='user name', example='admin'),
            'password': fields.String(required=True, description='user password', example='password')
        },
        mask="{*}"
    )

    model_auth: Model = namespace.model(
        "Auth",
        {
            "username": fields.String(required=True, description='user name', example='admin'),
            "token": fields.String(description='user token'),
            "joined_date": fields.Integer(description='user joined time', attribute='created'),
            "update_date": fields.Integer(description='user info updated time', attribute='updated'),
        },
        mask="{*}"
    )

    model_resp: Model = Dto.set_resp(namespace, model_auth)
