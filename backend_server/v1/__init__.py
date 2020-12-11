from flask import Blueprint
from flask_restx import Api

from backend_server.v1.user.dto import AccountDto

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          version='1.0',
          title='Backend Server API.',
          description='Flask Server: restful API server.',
          security='Bearer Auth')

api.add_namespace(AccountDto.namespace)
