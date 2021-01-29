from flask import Blueprint
from flask_restx import Api

from backend_server.v1.auth.dto import AuthDto

# https://flask-restx.readthedocs.io/en/latest/swagger.html?highlight=authorizations#documenting-authorizations
# https://swagger.io/docs/specification/2-0/authentication/
authorizations = {
    'ACCESS-CSRF-TOKEN': {
        'type': 'apiKey',
        'in': 'header',  # header query
        'name': 'ACCESS-CSRF-TOKEN'
    },
    'FRESH-CSRF-TOKEN': {
        'type': 'apiKey',
        'in': 'header',  # header query
        'name': 'ACCESS-CSRF-TOKEN'
    },
    'REFRESH-CSRF-TOKEN': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'REFRESH-CSRF-TOKEN'
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
           security='REFRESH-CSRF-TOKEN',
           authorizations=authorizations
           )

api_v1 = Api(api_v1_blueprint,
             version='1.0',
             title='Backend Server(API).',
             description='Flask Server: restful API server.',
             security='ACCESS-CSRF-TOKEN',
             authorizations=authorizations
             )

# add auth resource
auth.add_namespace(AuthDto.namespace)
