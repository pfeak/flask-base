from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource

from backend_server.common.response import error
from backend_server.v1.auth.dto import AuthDto
from backend_server.v1.auth.service import AuthService
from backend_server.v1.auth.utils import LoginSchema

api = AuthDto.namespace
login_schema = LoginSchema()


@api.route('/register')
class RegisterRsrc(Resource):
    @api.expect(AuthDto.model_login)
    @api.marshal_with(AuthDto.model_resp, code=201, description='user created', skip_none=True)
    def post(self):
        """user create"""
        data = request.get_json()

        if err := login_schema.validate(data):
            return error(400, err)

        return AuthService.register(data)


@api.route('/login')
class LoginRsrc(Resource):
    @api.expect(AuthDto.model_login)
    @api.marshal_with(AuthDto.model_resp, code=201, description='success')
    def post(self):
        """user login"""
        data = request.get_json()

        if err := login_schema.validate(data):
            return error(400, err)

        return AuthService.login(data)


@api.route('/logout')
class LogoutRsrc(Resource):
    @api.expect(AuthDto.model_login)
    @api.marshal_with(AuthDto.model_resp, code=201, description='success')
    @jwt_required
    def post(self):
        """user logout"""
        return "user logout", 200
