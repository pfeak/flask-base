from flask import Blueprint
from flask_restx import Api

from backend_server.v1.auth.dto import AuthDto
from backend_server.v1.user.dto import UserDto

# https://flask-restx.readthedocs.io/en/latest/swagger.html?highlight=authorizations#documenting-authorizations
# https://swagger.io/docs/specification/2-0/authentication/
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'cookie',
        'name': 'Authorization'
    },
    'X-CSRF-TOKEN': {
        'type': 'apiKey',
        'in': 'header',  # header query
        'name': 'X-CSRF-TOKEN'
    },
    'apiId': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'refresh_csrf'
    },
    # 'oauth2': {
    #     'type': 'oauth2',
    #     'flow': 'accessCode',
    #     'tokenUrl': 'https://somewhere.com/token',
    #     'authorizationUrl': 'https://somewhere.com/auth',
    #     'scopes': {
    #         'read': 'Grant read-only access',
    #         'write': 'Grant read-write access',
    #     }
    # }
}

auth_blueprint = Blueprint('auth', __name__)
api_v1_blueprint = Blueprint('api_v1', __name__)

auth = Api(auth_blueprint,
           version='1.0',
           title='Backend Server(AUTH).',
           description='Flask Server: restful API server.',
           security='X-CSRF-TOKEN',
           authorizations=authorizations
           )

api_v1 = Api(api_v1_blueprint,
             version='1.0',
             title='Backend Server(API).',
             description='Flask Server: restful API server.',
             security='X-CSRF-TOKEN',
             authorizations=authorizations
             )

# add auth resource
auth.add_namespace(AuthDto.namespace)

# add api resource
api_v1.add_namespace(UserDto.namespace)
