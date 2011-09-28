from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy.sql import functions
from sqlalchemy.orm import synonym
from s4u.sqlalchemy.meta import BaseObject
from s4u.sqlalchemy import meta
import cryptacular.bcrypt

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

def hash_password(password):
    return unicode(crypt.encode(password))

class User(BaseObject):
    __tablename__ = 'users'

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    username = schema.Column(types.Unicode(32), nullable=False, unique=True)
    email = schema.Column(types.String(256), nullable=False)
    _password = schema.Column('password', types.Unicode(255), nullable=False)
    created = schema.Column(types.DateTime(), nullable=False, default=functions.now())

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password) 

    @classmethod
    def check_emailpassword(cls, email, password):
        user = meta.Session.query(cls).filter(cls.email==email).first()
        if user:
            return crypt.check(user.password, password)
        else:
            return False

    @classmethod
    def check_usernamepassword(cls, username, password):
        user = meta.Session.query(cls).filter(cls.username==username).first()
        if user:
            return crypt.check(user.password, password)
        else:
            return False
