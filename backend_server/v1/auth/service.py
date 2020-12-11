from flask_jwt_extended import create_access_token

from backend_server import db
from backend_server.common.response import error, success
from backend_server.models.user import UserModel
from backend_server.v1.auth.utils import LoginSchema
from backend_server.v1.config import DEFAULT_HOURS


class AuthService:
    @staticmethod
    def register(data, hours: int = DEFAULT_HOURS):
        username = data.get("username")
        password = data.get("password")

        # Check if the username is taken
        if UserModel.query.filter_by(username=username).first() is not None:
            error(403, "Username is already being used.")

        try:
            new_user: UserModel = UserModel(username=username, password=password)

            db.session.add(new_user)
            db.session.commit()

            login_schema = LoginSchema(hours)

            return success(201, "User registration is successful.", login_schema.dump(new_user))
        except Exception as e:
            return error(500, e.args[0])

    @staticmethod
    def login(data, hours: int = DEFAULT_HOURS):
        username = data.get("username")
        password = data.get("password")

        if not (user := UserModel.query.filter_by(username=username).first()):
            error(403, "Username is not exists.")

        if not user.verify_password(password):
            error(403, "password is error.")

        login_schema = LoginSchema(hours)

        access_token = create_access_token(identity=username)
        user.token = access_token

        return success(201, "User login success.", login_schema.dump(user))


# @staticmethod
# def modify(data, hours: int = 0):
#     username = data.get("username")
#     alias = data.get("alias")
#
#     try:
#         user: UserModel = UserModel.query.filter_by(username=username).first()
#         if not user:
#             return error(404, "User is not exist.")
#
#         user.alias = alias
#
#         db.session.commit()
#
#         user_schema = UserSchema(hours)
#
#         new_user = user_schema.dump(user)
#
#         return success(201, "User modify success.", new_user)
#     except Exception as e:
#         current_app.logger.error(e)
#         return error(500, e.args[0])
