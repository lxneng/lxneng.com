from pyramid.exceptions import NotFound
from s4u.sqlalchemy import meta
from lxneng.models.post import Post
from lxneng.models.post import Tag
from lxneng.models.photo import Album
from pyramid.security import Everyone
from pyramid.security import Authenticated
from pyramid.security import Allow


def get_factory(cls):
    def factory(request):
        id = request.matchdict['id']
        result = meta.Session.query(cls).get(id)
        if result is None:
            raise NotFound('Unknown id')
        return result

    return factory


PostFactory = get_factory(Post)
AlbumFactory = get_factory(Album)
TagFactory = get_factory(Tag)


class RootFactory(object):
    __acl__ = [
            (Allow, Everyone, 'view'),
            (Allow, Authenticated, 'auth')
    ]

    def __init__(self, request):
        pass
