from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims, fresh_jwt_required, \
    jwt_refresh_token_required
from flask_restx import Resource

from backend_server.common.response import error
from backend_server.v1.auth.dto import AuthDto
from backend_server.v1.auth.service import AuthService
from backend_server.v1.auth.utils import LoginSchema

api = AuthDto.namespace
login_schema = LoginSchema()


@api.route('/register')
class AccountRegisterRsrc(Resource):
    @api.expect(AuthDto.auth_login)
    @api.marshal_with(AuthDto.auth_resp, code=201, description='user created', skip_none=True)
    def post(self):
        """user create"""
        data = request.get_json()

        if err := login_schema.validate(data):
            return error(400, err)

        return AuthService.register(data)


@api.route('/login')
class AccountLoginRsrc(Resource):
    @api.expect(AuthDto.auth_login)
    @api.marshal_with(AuthDto.auth_resp, code=201, description='success')
    def post(self):
        """user login"""
        data = request.get_json()

        if err := login_schema.validate(data):
            return error(400, err)

        return AuthService.login(data)


@api.route('/logout')
class AccountLogoutRsrc(Resource):
    @api.marshal_with(AuthDto.auth_resp, code=200, description='success')
    @jwt_required
    def post(self):
        """user logout"""
        return AuthService.logout()


@api.route('/refresh')
class AccountRefreshRsrc(Resource):
    @api.marshal_with(AuthDto.auth_resp, code=200, description='success')
    @jwt_refresh_token_required
    def get(self):
        """user access token refresh"""
        refresh_token = request.headers.environ['HTTP_AUTHORIZATION'].split(' ')[-1]
        return AuthService.refresh(refresh_token)


@api.route('/account')
class AccountRsrc(Resource):
    @fresh_jwt_required
    def post(self):
        """modify account auth info(eg. username or password)"""
