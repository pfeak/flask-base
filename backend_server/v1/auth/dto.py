from flask_restx import Model, fields, Namespace

from backend_server.v1.common.dto import Dto, CommonUserDto


class AuthDto:
    namespace = Namespace('token', path='/token', description='token related api')

    auth_login: Model = namespace.model(
        'Auth-login',
        {
            'username': fields.String(required=True, description='user name', example='admin'),
            'password': fields.String(required=True, description='user password', example='password')
        },
        mask="{*}"
    )

    auth_user: Model = namespace.model(
        "Auth",
        {
            "user": fields.Nested(CommonUserDto.user_model),
            "access_token": fields.String(description='access token'),
            "refresh_token": fields.String(description='refresh token'),
        },
        mask="{*}"
    )
    # register models
    namespace.models[CommonUserDto.user_model.name] = CommonUserDto.user_model

    auth_resp: Model = Dto.set_resp(namespace, auth_user)
