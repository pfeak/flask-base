from flask_jwt_extended import jwt_required
from flask_restx import Resource

from backend_server.common.response import error
from backend_server.v1.user.dto import UserDto
from backend_server.v1.user.service import AccountService
from backend_server.v1.user.utils import UserSchema

api = UserDto.namespace
user_schema = UserSchema()


@api.route('/<string:username>')
class UserRsrc(Resource):
    @api.expect(UserDto.request_patch_user)
    @api.marshal_with(UserDto.model_resp, code=201, description='user modified', skip_none=True)
    def patch(self, username):
        """modify user info"""
        data = UserDto.request_patch_user.parse_args()
        data.setdefault('username', username)
        hours = data.pop('hours') if data.get('hours') else 0
        hours = hours if hours > 0 else 0

        if err := user_schema.validate(data):
            return error(400, err)

        return AccountService.modify(data, hours)

    @api.expect(UserDto.request_get_user)
    @api.marshal_with(UserDto.model_resp, code=200, description='success', skip_none=True)
    def get(self, username):
        """get user info"""
        data = UserDto.request_get_user.parse_args()
        hours = data.pop('hours') if data.get('hours') else 0
        hours = hours if hours > 0 else 0

        return AccountService.get_user(username, hours)


@api.route('/account')
class AccountRsrc(Resource):
    # @fresh_jwt_required
    @jwt_required
    def post(self):
        """modify account auth info(eg. username or password)"""