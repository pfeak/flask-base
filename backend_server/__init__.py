import datetime
import logging
import os
import sys

from flask import Flask
from gevent import monkey
from loguru import logger

from backend_server.common import g_config
from backend_server.extensions import db, bc, jwt, migrate, redis

# monkey.patch_all()

config_by_name = dict(
    dev="dev.cfg",
    test="test.cfg",
    prod="prod.cfg",
    default="dev.cfg",
)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


def register_logger(server):
    try:
        logger.remove(0)
    except ValueError:
        pass

    fmt = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> ' \
          '| <level>{level: <6}</level> | {name} - <level>{message}</level>'

    # add normal logger
    logger.add(sys.stdout, colorize=True, format=fmt, level=server.config['LOG_LEVEL'])
    # add file logger
    logger.add(
        # './log/runtime_{time}.log',
        './log/runtime.log',
        enqueue=True,
        rotation='10 MB',
        retention='30 days',
        level=server.config['LOG_LEVEL'])

    # replace root logger
    if len(server.logger.handlers) != 0:
        server.logger.removeHandler(server.logger.handlers[0])
    server.logger.root.addHandler(InterceptHandler())


def register_globals(server):
    g_config['JWT_ACCESS_EXPIRE'] = server.config['JWT_ACCESS_TOKEN_EXPIRES']
    g_config['JWT_REFRESH_EXPIRE'] = server.config['JWT_REFRESH_TOKEN_EXPIRES']
    g_config['TIME_ZONE'] = int(server.config['TIME_ZONE'])


def register_extensions(server):
    """Register flask extensions"""
    register_logger(server)
    db.init_app(server)
    migrate.init_app(server)
    bc.init_app(server)
    jwt.init_app(server)
    redis.init_app(server)
    server.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=server.config['JWT_ACCESS_EXPIRE'])
    server.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=server.config['JWT_REFRESH_EXPIRE'])


def create_app():
    # todo: 配置文件 *
    # todo: 异常报错处理 *
    # todo: 返回接口包裹 *
    # todo: 错误返回解析地址提示关闭 *
    # todo: 鉴权
    # todo: 后台管理
    # todo: 日志 *
    server = Flask(__name__)

    dirname = os.getenv("CONFIG_DIR_NAME_FOR_DYNAMIC", default="config")
    mode = os.getenv("CONFIG_MODE", default="default")
    server.config.from_pyfile(os.path.join(os.getcwd(), dirname, config_by_name[mode]))

    # Register extensions
    register_extensions(server)

    # Register global variables
    register_globals(server)

    # Register blueprints
    from backend_server.v1 import auth_blueprint
    from backend_server.v1 import api_v1_blueprint

    server.register_blueprint(auth_blueprint, url_prefix='/s/token')
    server.register_blueprint(api_v1_blueprint, url_prefix='/s/api/v1')

    # Create tables is not exist
    with server.app_context():
        db.create_all()

    return server
