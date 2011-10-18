from sqlalchemy import schema
from sqlalchemy import types
from s4u.sqlalchemy.meta import BaseObject
from sqlalchemy.sql import functions
from pyramid.security import Authenticated
from pyramid.security import Allow


class Post(BaseObject):

    __tablename__ = 'wp_posts'
    __acl__ = [(Allow, Authenticated, 'auth')]

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    title = schema.Column('post_title', types.String(256), nullable=False)
    content = schema.Column('post_content', types.Text, nullable=False)
    status = schema.Column('post_status', types.String(20), nullable=False,
            default='publish')
    created_at = schema.Column('post_date', types.DateTime(), nullable=False,
            default=functions.now())
