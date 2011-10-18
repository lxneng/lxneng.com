import markdown
from pyramid.security import authenticated_userid
from s4u.sqlalchemy import meta
from lxneng.models import User


class Tools(object):
    """A collection of tools that can be used in templates."""

    def __init__(self, request):
        self.request = request
        
    def markdown_content(self, content):
        return markdown.markdown(content, ['codehilite'])


def get_user(request):

    user = getattr(request, '_user', [])
    if not user:
        user_id = authenticated_userid(request)
        if user_id is None:
            return None
        else:
            user = meta.Session.query(User).get(user_id)
            request._user = user
    return user
