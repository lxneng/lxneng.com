from pyramid.exceptions import NotFound
from s4u.sqlalchemy import meta
from lxneng.models import Post


def SimpleTypeFactory(cls):
    def factory(request):
        id = request.matchdict.get('id')
        if id is None:
            raise NotFound('Missing id')
        if not id.isdigit():
            raise NotFound('Invalid id')

        result = meta.Session.query(cls).get(id)
        if result is None:
            raise NotFound('Unknown id')
        return result

    return factory


PostFactory = SimpleTypeFactory(Post)
