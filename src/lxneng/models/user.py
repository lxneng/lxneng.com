from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy.sql import functions
from sqlalchemy.orm import synonym
from s4u.sqlalchemy.meta import BaseObject
from s4u.sqlalchemy import meta
import bcrypt


class User(BaseObject):
    __tablename__ = 'users'

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    username = schema.Column(types.Unicode(32), nullable=False, unique=True)
    email = schema.Column(types.String(256), nullable=False)
    _password = schema.Column('password', types.Unicode(255), nullable=False)
    created_at = schema.Column(types.DateTime(),
            nullable=False, default=functions.now())
    updated_at = schema.Column(types.DateTime(),
            nullable=False, default=functions.now())

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = bcrypt.hashpw(password, bcrypt.gensalt())

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)

    def authenticate(self, password):
        return bcrypt.hashpw(password, self.password) == self.password

    @classmethod
    def check_emailpassword(cls, email, password):
        user = meta.Session.query(cls).filter(cls.email == email).first()
        if user:
            return bcrypt.hashpw(password, user.password) == user.password
        else:
            return False

    @classmethod
    def check_usernamepassword(cls, username, password):
        user = meta.Session.query(cls).filter(cls.username == username).first()
        if user:
            return bcrypt.hashpw(password, user.password) == user.password
        else:
            return False
