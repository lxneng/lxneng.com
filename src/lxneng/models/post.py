from sqlalchemy import schema
from sqlalchemy import types
from s4u.sqlalchemy.meta import BaseObject
from sqlalchemy.sql import functions
from sqlalchemy import orm
from pyramid.security import Authenticated
from pyramid.security import Allow
from s4u.sqlalchemy import meta


posts_tags = schema.Table("posts_tags", meta.metadata,
        schema.Column("post_id", types.Integer,
            schema.ForeignKey("posts.id", ondelete='CASCADE')),
        schema.Column("tag_id", types.Integer,
            schema.ForeignKey("tags.id", ondelete='CASCADE')))


class Post(BaseObject):

    __tablename__ = 'posts'
    __acl__ = [(Allow, Authenticated, 'auth')]

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    title = schema.Column(types.String(256), nullable=False)
    summary = schema.Column(types.String(256))
    content = schema.Column(types.Text, nullable=False)
    status = schema.Column(types.String(20), nullable=False,
            default='publish')
    tags = orm.relationship('Tag', secondary=posts_tags)
    created_at = schema.Column(types.DateTime(), nullable=False,
            default=functions.now())
    updated_at = schema.Column(types.DateTime(), nullable=False,
            default=functions.now())


class Tag(BaseObject):

    __tablename__ = 'tags'

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    name = schema.Column(types.String(32), index=True)
    posts = orm.relationship('Post', secondary=posts_tags)
