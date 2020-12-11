from typing import Union

from flask_restx import abort
from loguru import logger


def message(code: int = 200, msg: str = ""):
    response_object = {"status": code, "message": msg}
    return response_object


def success(code: int = 200, msg: str = "", data=None):
    """Response of success"""
    logger.success(msg)
    if data:
        obj = message(code, msg)
        obj["data"] = data
    else:
        obj = message(code, msg)
    return obj, code


def error(code: int = 400, msg: Union[str, dict] = "", data=None):
    """abort error response"""
    logger.error(msg)
    if data:
        abort(code, status=code, data=data, message=msg)
    else:
        abort(code, status=code, message=msg)
