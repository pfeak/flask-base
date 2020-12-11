from flask import current_app

from backend_server import db
from backend_server.common.response import error, success
from backend_server.models.user import UserModel
from backend_server.v1.user.utils import UserSchema


class AccountService:
    @staticmethod
    def get_user(username, hours: int = 8):
        """Get user data by username"""
        user: UserModel = UserModel.query.filter_by(username=username).first()
        if not user:
            return error(404, "User is not exist.")

        user_schema = UserSchema(hours)

        new_user = user_schema.dump(user)

        return success(200, "User info got success.", new_user)

    @staticmethod
    def modify(data, hours: int = 0):
        username = data.get("username")
        alias = data.get("alias")

        try:
            user: UserModel = UserModel.query.filter_by(username=username).first()
            if not user:
                return error(404, "User is not exist.")

            user.alias = alias

            db.session.commit()

            user_schema = UserSchema(hours)

            new_user = user_schema.dump(user)

            return success(201, "User modify success.", new_user)
        except Exception as e:
            current_app.logger.error(e)
            return error(500, e.args[0])
