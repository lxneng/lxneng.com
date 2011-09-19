from sqlalchemy import schema
from sqlalchemy import types
from s4u.sqlalchemy.meta import BaseObject


class Post(BaseObject):

    __tablename__ = 'wp_posts'

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    post_title = schema.Column(types.String(256), nullable=False)
    post_content = schema.Column(types.Text, nullable=False)
    post_status = schema.Column(types.String(20), nullable=False)
    post_date = schema.Column(types.DateTime(), nullable=False)
