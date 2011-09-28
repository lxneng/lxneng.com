import os
import logging
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import remember
from pyramid.security import forget 
from s4u.sqlalchemy import meta
from lxneng.models import Post
from lxneng.models import User
from itertools import groupby
from pyramid.url import route_url
from pyramid.httpexceptions import HTTPFound

log = logging.getLogger(__name__)

_here = os.path.dirname(__file__)
_robots = open(os.path.join(_here, '../static', 'robots.txt')).read()
_robots_response = Response(content_type='text/plain', body=_robots)
_favicon = open(os.path.join(_here, '../static', 'favicon.ico')).read()
_favicon_response = Response(content_type='image/x-icon', body=_favicon)


@view_config(route_name='photos', renderer='photos.html')
@view_config(route_name='about', renderer='about.html')
@view_config(route_name='post', renderer='post.html')
@view_config(context='pyramid.exceptions.NotFound', renderer='404.html')
@view_config(context='pyramid.exceptions.HTTPForbidden', renderer='403.html')
class BaseHandler(object):

    def __init__(self, context, request):
        self.request = request
        self.context = context
        locale_name = request.params.get('lang', False)
        session = request.session
        if locale_name:
            session['lang'] = locale_name
            self.request.locale_name = locale_name
        else:
            self.request.locale_name = session.get('lang', 'en')

    def __call__(self):
        return {'context': self.context}


@view_config(name='robots.txt')
def robotstxt_view(context, request):
    return _robots_response


@view_config(name='favicon.ico')
def favicon_view(context, request):
    return _favicon_response


@view_config(route_name='login', renderer='login.html')
class Login(BaseHandler):
    def login(self):
        login_url = route_url('login', self.request)
        referrer = self.request.url
        if referrer == login_url:
            referrer = route_url('home', self.request)
        came_from = self.request.params.get('came_from', referrer)

        session = meta.Session()
        login = self.request.POST['login']
        password = self.request.POST['password']
        query = session.query(User)
        user = query.filter(User.username == login).first()\
                or query.filter(User.email == login).first()
        if user is not None and user.authenticate(password):
            log.info('%s login' % user.username)
            headers = remember(self.request, user.username)
            return HTTPFound(location=route_url('home', self.request),
                             headers=headers)
        else:
            return HTTPFound(localtion=came_from)

    def __call__(self):
        if self.request.method == 'POST':
            return self.login()
        return {}

@view_config(route_name='logout')
def logout(request):
    came_from = request.params.get('url', route_url('home', request))
    request.session.invalidate()
    request.session.flash('Logged out')
    headers = forget(request)
    return HTTPFound(location=came_from, headers=headers)

@view_config(route_name='blog', renderer='blog.html')
class Blog(BaseHandler):
    def __call__(self):

        def grouper(item):
            return item.post_date.year, item.post_date.month

        posts = meta.Session.query(Post)\
                .filter(Post.post_status == 'publish')\
                .order_by(Post.id.desc()).all()
        result = groupby(posts, grouper)
        return {'result': result}


@view_config(route_name='home', renderer='home.html')
class Home(BaseHandler):
    def __call__(self):
        posts = meta.Session.query(Post)\
                .filter(Post.post_status == 'publish')\
                .order_by(Post.id.desc()).limit(10)
        return {'posts': posts}
