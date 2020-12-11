from flask import request
from flask_restx import Resource

from backend_server.common.response import error
from backend_server.v1.user.dto import AccountDto
from backend_server.v1.user.service import AccountService
from backend_server.v1.user.utils import UserSchema

api = AccountDto.namespace
user_schema = UserSchema()


@api.route('/<string:username>')
class UserRsrc(Resource):
    @api.expect(AccountDto.request_patch_user)
    @api.marshal_with(AccountDto.model_resp, code=201, description='user modified', skip_none=True)
    def patch(self, username):
        """modify user info"""
        data = AccountDto.request_patch_user.parse_args()
        data.setdefault('username', username)
        hours = data.pop('hours') if data.get('hours') else 0
        hours = hours if hours > 0 else 0

        if err := user_schema.validate(data):
            return error(400, err)

        return AccountService.modify(data, hours)

    @api.expect(AccountDto.request_get_user)
    @api.marshal_with(AccountDto.model_resp, code=200, description='success', skip_none=True)
    def get(self, username):
        """get user info"""
        data = AccountDto.request_get_user.parse_args()
        hours = data.pop('hours') if data.get('hours') else 0
        hours = hours if hours > 0 else 0

        return AccountService.get_user(username, hours)


@api.route('/register')
class RegisterRsrc(Resource):
    @api.expect(AccountDto.model_login)
    @api.marshal_with(AccountDto.model_resp, code=201, description='user created', skip_none=True)
    def post(self):
        """create new user"""
        data = request.get_json()

        if err := user_schema.validate(data, partial=("alias",)):
            return error(400, err)

        return AccountService.register(data)


@api.route('/login')
class LoginRsrc(Resource):
    @api.expect(AccountDto.model_login)
    @api.marshal_with(AccountDto.model_resp, code=201, description='success')
    def post(self):
        """user login"""
        return "user login", 200


@api.route('/logout')
class LogoutRsrc(Resource):
    @api.expect(AccountDto.model_user)
    @api.marshal_with(AccountDto.model_resp, code=201, description='success')
    def post(self):
        """user logout"""
        return "user logout", 200
