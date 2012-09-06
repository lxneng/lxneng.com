from sqlalchemy import schema
from sqlalchemy import types
from easy_sqlalchemy.meta import BaseObject
from sqlalchemy.sql import functions
from sqlalchemy import orm
from pyramid.security import Authenticated
from pyramid.security import Allow
from easy_sqlalchemy import meta


posts_tags = schema.Table('posts_tags', meta.metadata,
                          schema.Column('post_id', types.Integer,
                                        schema.ForeignKey(
                                            'posts.id', ondelete='CASCADE')),
                          schema.Column('tag_id', types.Integer,
                                        schema.ForeignKey('tags.id', ondelete='CASCADE')))


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

    @property
    def tags_string(self):
        return ' '.join([t.name for t in self.tags])


class Tag(BaseObject):

    __tablename__ = 'tags'

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    name = schema.Column(types.String(32), index=True)
    posts = orm.relationship('Post', secondary=posts_tags, lazy='dynamic')

    @staticmethod
    def extract_tags(tags_string):
        tags = tags_string.replace(';', ' ').replace(',', ' ')
        tags = [tag for tag in tags.split()]
        tags = set(tags)
        return tags

    @classmethod
    def find_by_name(cls, tag_name):
        return meta.Session.query(cls).filter(cls.name == tag_name).first()

    @classmethod
    def create_tags(cls, tags_string):
        session = meta.Session()
        tags_list = cls.extract_tags(tags_string)
        tags = []

        for tag_name in tags_list:
            tag = cls.find_by_name(tag_name)
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
            tags.append(tag)

        return tags

    @classmethod
    def tag_counts(cls):
        query = meta.Session.query(cls.name, functions.count('*'))
        return query.join('posts').group_by(cls.name)
