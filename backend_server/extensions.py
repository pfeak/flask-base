"""
Extensions module

Each extensions is initialized when app is created.
"""
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate(db=db)
bc = Bcrypt()
jwt = JWTManager()
