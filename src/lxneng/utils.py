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
    username = authenticated_userid(request)
    user = meta.Session.query(User).filter(User.username ==
            username).first()
    return user
