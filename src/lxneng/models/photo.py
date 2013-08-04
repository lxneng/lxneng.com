import os
from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy import orm
from easy_sqlalchemy.meta import BaseObject
from sqlalchemy.sql import functions
from pyramid.security import Authenticated
from pyramid.security import Allow
from repoze.filesafe import create_file


class Album(BaseObject):

    __tablename__ = 'albums'
    __acl__ = [(Allow, Authenticated, 'auth')]

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    title = schema.Column(types.String(256), nullable=False)
    description = schema.Column(types.Text, nullable=False)
    flickr_set_id = schema.Column(types.String(32), index=True)
    photos = orm.relationship('Photo', order_by='Photo.id.desc()',
                              lazy='dynamic', backref='album')
    created_at = schema.Column(types.DateTime(),
                               nullable=False, default=functions.now())
    updated_at = schema.Column(types.DateTime(),
                               nullable=False, default=functions.now(), index=True)

    @property
    def primary_photo(self):
        return self.photos.filter(Photo.is_primary == True).first()


class Photo(BaseObject):

    __tablename__ = 'photos'
    __acl__ = [(Allow, Authenticated, 'auth')]

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    path = schema.Column(types.String(128), nullable=False, unique=True)
    description = schema.Column(types.String(256), nullable=False)
    is_primary = schema.Column(types.Boolean(), default=False)
    flickr_photo_id = schema.Column(types.String(32), index=True)
    album_id = schema.Column(types.Integer(), schema.ForeignKey(Album.id))
    created_at = schema.Column(types.DateTime(),
                               nullable=False, default=functions.now())
    updated_at = schema.Column(types.DateTime(),
                               nullable=False, default=functions.now(), index=True)

    def set_image(self, data=None, filename=None):
        if data is None:
            self.path = filename or '/dev/null'
            return
        if not os.path.isdir(os.path.join(self.root_path, self.album_id)):
            os.mkdir(os.path.join(self.root_path, self.album_id))
        self.path = os.path.join(self, filename)
        img = create_file(self.filesystem_path, 'wb')
        if hasattr(img, 'fileno'):
            os.fchmod(img.fileno(), 0644)
        img.write(data)
        img.close()

    @property
    def filesystem_path(self):
        if self.root_path is None:
            raise AttributeError('root_path not set')
        return os.path.join(self.root_path, self.path)
