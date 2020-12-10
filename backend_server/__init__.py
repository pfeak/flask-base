import os

from flask import Flask
from gevent import monkey

from backend_server.extensions import db, bc

# monkey.patch_all()

config_by_name = dict(
    dev="dev.cfg",
    test="test.cfg",
    prod="prod.cfg",
    default="dev.cfg",
)


def create_app():
    # todo: 配置文件
    # todo: 异常报错处理 *
    # todo: 返回接口包裹
    # todo: 错误返回解析地址提示关闭 *
    # todo: 鉴权
    # todo: 后台管理
    server = Flask(__name__)

    dirname = os.getenv("CONFIG_DIR_NAME_FOR_DYNAMIC", default="config")
    mode = os.getenv("CONFIG_MODE", default="default")
    server.config.from_pyfile(os.path.join(os.getcwd(), dirname, config_by_name[mode]))

    server.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    server.config['RESTX_MASK_HEADER'] = 'SP-Fields'  # 修改 mask 为其他, 默认 'X-Fields'
    server.config['RESTX_MASK_SWAGGER'] = False  # 是否在 swagger ui 中开启 mask 模式(实际上关闭后也可以传 mask)
    # server.config['BUNDLE_ERRORS'] = False  # parse 提示所有错误
    server.config['RESTX_VALIDATE'] = True  # 开启 model 参数错误校验
    server.config['ERROR_404_HELP'] = False  # 关闭 404 返回的提示信息以免暴露接口
    server.config['ERROR_INCLUDE_MESSAGE'] = True  # 关闭错误提示信息

    # Register extensions
    register_extensions(server)

    # Register blueprints
    from backend_server.v1 import blueprint as api_v1_blueprint

    server.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    # Create tables is not exist
    with server.app_context():
        db.create_all()

    return server


def register_extensions(server):
    """Register flask extensions"""
    db.init_app(server)
    bc.init_app(server)
