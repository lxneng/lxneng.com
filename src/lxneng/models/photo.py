from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy import orm
from s4u.sqlalchemy.meta import BaseObject
from sqlalchemy.sql import functions
from s4u.image import Image

class Album(BaseObject):

    __tablename__ = 'albums'

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    name = schema.Column(types.String(256), nullable=False)
    description = schema.Column(types.String(512), nullable=False)
    photos = orm.relationship("Photo", backref="photos")
    created = schema.Column(types.DateTime(),
            nullable=False, default=functions.now())


class Photo(BaseObject):
    
    __tablename__ = 'photos'
    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    description = schema.Column(types.String(256), nullable=False)
    image_id = schema.Column(types.Integer(),
            schema.ForeignKey(Image.id,
                onupdate="CASCADE", ondelete="RESTRICT"),
            unique=True)
    image = orm.relationship(Image, cascade="all")
    album_id = schema.Column(types.Integer(), schema.ForeignKey(Album.id))
    album = orm.relationship(Album, backref='albums')
    created = schema.Column(types.DateTime(),
            nullable=False, default=functions.now())