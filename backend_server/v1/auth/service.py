from flask_jwt_extended import create_access_token, create_refresh_token, get_jti, get_jwt_identity, get_raw_jwt

from backend_server import db, redis, g_config
from backend_server.common.response import error, success
from backend_server.models.user import UserModel
from backend_server.v1.auth.utils import LoginSchema

ACCESS_EXPIRE = g_config['JWT_ACCESS_EXPIRE'] * 1.2
REFRESH_EXPIRE = g_config['JWT_REFRESH_EXPIRE'] * 1.2
login_schema = LoginSchema(g_config['TIME_ZONE'])


class AuthService:
    @staticmethod
    def register(data):
        username = data.get("username")
        password = data.get("password")

        # Check if the username is taken
        if UserModel.query.filter_by(username=username).first() is not None:
            error(403, "Username is already being used.")

        try:
            new_user: UserModel = UserModel(username=username, password=password)

            db.session.add(new_user)
            db.session.commit()

            return success(201, "User registration is successful.", login_schema.dump(new_user))
        except Exception as e:
            error(500, e.args[0])

    @staticmethod
    def login(data):
        username = data.get("username")
        password = data.get("password")

        if not (user := UserModel.query.filter_by(username=username).first()):
            error(403, "Username is not exists.")

        if not user.verify_password(password):
            error(403, "password is error.")

        # access_token = create_access_token(identity=username, fresh=timedelta(seconds=20))
        # create token
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        # update redis
        access_jti = get_jti(encoded_token=access_token)
        refresh_jti = get_jti(encoded_token=refresh_token)
        redis.set(access_jti, 'false', ACCESS_EXPIRE)
        redis.set(refresh_jti, 'false', REFRESH_EXPIRE)

        response = {
            'user': user,
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return success(201, "User login success.", login_schema.dump(response))

    @staticmethod
    def logout():
        # todo: logout 的时候 access 和 refresh 都需要拉黑
        jti = get_raw_jwt()['jti']
        redis.set(jti, 'true', ACCESS_EXPIRE)

        # get user info
        username = get_jwt_identity()
        if not (user := UserModel.query.filter_by(username=username).first()):
            error(403, "Username is not exists.")

        response = {
            'user': user
        }

        return success(200, "User logout success.", login_schema.dump(response))

    @staticmethod
    def refresh(refresh_token):
        # create new access token
        username = get_jwt_identity()
        access_token = create_access_token(identity=username)
        access_jti = get_jti(encoded_token=access_token)
        redis.set(access_jti, 'false', ACCESS_EXPIRE)
        # get user info
        if not (user := UserModel.query.filter_by(username=username).first()):
            error(403, "Username is not exists.")

        response = {
            'user': user,
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return success(200, "User login success.", login_schema.dump(response))
