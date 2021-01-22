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
    @api.doc(security=[])
    @api.expect(AuthDto.auth_login)
    @api.marshal_with(AuthDto.auth_resp, code=201, description='user created', skip_none=True)
    def post(self):
        """User create"""
        data = request.get_json()

        if err := login_schema.validate(data):
            return error(400, err)

        return AuthService.register(data)


@api.route('/login')
class AccountLoginRsrc(Resource):
    @api.doc(security=[])
    @api.expect(AuthDto.auth_login)
    @api.response(code=201, description='success', model=AuthDto.auth_resp)
    def post(self):
        """User login"""
        data = request.get_json()

        if err := login_schema.validate(data):
            return error(400, err)

        return AuthService.login(data)


@api.route('/logout')
class AccountLogoutRsrc(Resource):
    @api.doc(security=['ACCESS-CSRF-TOKEN', 'REFRESH-CSRF-TOKEN'])
    @api.marshal_with(AuthDto.auth_resp, code=204, description='success')
    @jwt_required
    @jwt_refresh_token_required
    def delete(self):
        """User logout"""
        return AuthService.logout(
            request.cookies['access_token_cookie'],
            request.cookies['refresh_token_cookie']
        )


@api.route('/refresh/access')
class AccountRefreshRsrc(Resource):
    @api.response(code=201, description='success', model=AuthDto.auth_resp)
    @jwt_refresh_token_required
    def post(self):
        """User one-time access token"""
        return AuthService.refresh(request.cookies['refresh_token_cookie'])


@api.route('/refresh/fresh_access')
class AccountFreshRsrc(Resource):
    @api.doc(security=['ACCESS-CSRF-TOKEN', 'REFRESH-CSRF-TOKEN'])
    @api.response(code=201, description='success', model=AuthDto.auth_resp)
    @jwt_refresh_token_required
    @jwt_required
    def post(self):
        """User one-time fresh access token"""
        return AuthService.fresh(
            request.cookies['access_token_cookie'],
            request.cookies['refresh_token_cookie']
        )


@api.route('/test1')
class TestRsrc(Resource):
    @api.doc(security='ACCESS-CSRF-TOKEN')
    @jwt_required
    def get(self):
        """Fresh access token test"""


@api.route('/test2')
class TestFreshRsrc(Resource):
    @api.doc(security=['ACCESS-CSRF-TOKEN', 'REFRESH-CSRF-TOKEN', 'FRESH-CSRF-TOKEN'])
    @jwt_required
    @fresh_jwt_required
    def get(self):
        """Dangerous operation test interface."""
