from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy import orm
from s4u.sqlalchemy.meta import BaseObject
from sqlalchemy.sql import functions


class Album(BaseObject):

    __tablename__ = 'albums'

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    title = schema.Column(types.String(256), nullable=False)
    description = schema.Column(types.Text, nullable=False)
    flickr_set_id = schema.Column(types.String(32), index=True)
    photos = orm.relationship("Photo", backref="photos")
    created = schema.Column(types.DateTime(),
            nullable=False, default=functions.now())


class Photo(BaseObject):

    __tablename__ = 'photos'

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    path = schema.Column(types.String(128), nullable=False, unique=True)
    description = schema.Column(types.String(256), nullable=False)
    is_cover = schema.Column(types.Boolean(), default=False)
    flickr_photo_id = schema.Column(types.String(32), index=True)
    album_id = schema.Column(types.Integer(), schema.ForeignKey(Album.id))
    album = orm.relationship(Album, backref='albums')
    created = schema.Column(types.DateTime(),
            nullable=False, default=functions.now())
