from datetime import datetime

from backend_server import db, bc

Column = db.Column
relationship = db.relationship


class UserModel(db.Model):
    """User model"""
    __tablename__ = 'user'

    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(64), unique=True, index=True)
    password_hash = Column(db.String(128), nullable=False)
    alias = Column(db.String(15), unique=True, index=True)
    created = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bc.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bc.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {column.name: value.timestamp() if isinstance(value, datetime) else value for column in
                self.__table__.columns if (value := getattr(self, column.name))}
