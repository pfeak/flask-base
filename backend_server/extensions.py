"""
Extensions module

Each extensions is initialized when app is created.
"""
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bc = Bcrypt()
jwt = JWTManager()
