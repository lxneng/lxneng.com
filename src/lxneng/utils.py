import markdown
from pyramid.security import authenticated_userid
from s4u.sqlalchemy import meta
from lxneng.models.user import User
from babel.dates import format_date
from jinja2 import Markup
from webhelpers.paginate import Page


def markdown2html(content):
    return Markup(markdown.markdown(content, ['codehilite']))


class Tools(object):
    """A collection of tools that can be used in templates."""

    def __init__(self, request):
        self.request = request

    def markdown_content(self, content):
        return markdown2html(content)

    def format_date(self, date=None, format="full"):
        return format_date(date, format, locale=self.request.locale_name)

    def paginate(self, items):
        current_page = self.request.GET.get('page') or 1
        def page_url(page):
            return self.request.current_route_url(_query={'page': page})
        return Page(items, current_page, url=page_url)


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
