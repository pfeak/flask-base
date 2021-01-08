from flask_restx import Model, fields, Namespace

from backend_server.v1.common.dto import Dto, CommonUserDto


class AuthDto:
    namespace = Namespace('auth', path='/', description='token related api')

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
            'access_csrf': fields.String(description='csrf access token'),
            'refresh_csrf': fields.String(description='csrf refresh token'),
        },
        mask="{*}"
    )
    # register models
    namespace.models[CommonUserDto.user_model.name] = CommonUserDto.user_model

    auth_resp: Model = Dto.set_resp(namespace, auth_user)
