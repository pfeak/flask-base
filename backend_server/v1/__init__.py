from flask import Blueprint
from flask_restx import Api

from backend_server.v1.auth.dto import AuthDto
from backend_server.v1.user.dto import UserDto


# https://flask-restx.readthedocs.io/en/latest/swagger.html?highlight=authorizations#documenting-authorizations
# https://swagger.io/docs/specification/2-0/authentication/
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',  # header query
        'name': 'X-API'
    },
    'apiId': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Y-API'
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

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          version='1.0',
          title='Backend Server API.',
          description='Flask Server: restful API server.',
          security='Bearer',
          authorizations=authorizations
          )

api.add_namespace(UserDto.namespace)
api.add_namespace(AuthDto.namespace)
