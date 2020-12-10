from flask_restx import Namespace, fields, Model


class Dto:
    @staticmethod
    def init(name: str, path: str = None, description: str = None):
        return Namespace(name, path=path, description=description)

    @staticmethod
    def set_resp(namespace: Namespace, model: Model = None):
        data = fields.Nested(model)
        return namespace.model(
            model.name + "-response",
            {
                'status': fields.Integer(description='status'),
                'message': fields.String(description='message'),
                'data': data if data else fields.Raw
            }
        )
