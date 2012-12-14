import os
import logging
from pyramid.view import view_config
from pyramid.security import remember
from pyramid.security import forget
from easy_sqlalchemy import meta
from lxneng.models.post import Post
from lxneng.models.user import User
from lxneng.models.photo import Photo
from pyramid.url import route_url
from pyramid.httpexceptions import HTTPFound
from flatland import Form, String
from flatland.validation import Present


log = logging.getLogger(__name__)

_here = os.path.dirname(__file__)
RESUME_EN = open(os.path.join(_here, '../static', 'Resume_EN.md')).read()
RESUME_CN = open(os.path.join(_here, '../static', 'Resume_CN.md'))\
    .read().decode('utf8')

@view_config(route_name='cse', renderer='cse.html')
@view_config(route_name='posts_tags_show', renderer='posts/tags/show.html')
@view_config(context='pyramid.exceptions.NotFound', renderer='404.html')
@view_config(context='pyramid.exceptions.URLDecodeError', renderer='404.html')
@view_config(context='pyramid.exceptions.HTTPForbidden', renderer='403.html')
class BasicView(object):

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
        return {}


class BasicFormView(BasicView):

    form_class = None

    def __init__(self, context, request):
        super(BasicFormView, self).__init__(context, request)
        if self.request.method == 'POST':
            self.form = self.form_class.from_flat(self.request.POST)
        else:
            self.form = self.form_class(self.default_data())

    def default_data(self):
        if self.context is None:
            return {}
        defaults = {}
        fields = list(self.form_class())
        for key in self.context.__dict__:
            if key not in fields:
                continue
            defaults[key] = getattr(self.context, key)
        return defaults

    def do_post(self):
        raise NotImplementedError()

    def __call__(self):
        if self.request.method == 'POST':
            response = self.do_post()
            if response is not None:
                return response
        return {'form': self.form}


class LoginForm(Form):
    login = String.using(label='Login', validators=[Present()])
    password = String.using(label='Password', validators=[Present()])
    came_from = String


@view_config(route_name='login', renderer='login.html')
class Login(BasicFormView):

    form_class = LoginForm

    def do_post(self):
        if not self.form.validate():
            return None
        data = self.form.value
        login_url = route_url('login', self.request)
        came_from = data.pop('came_from')
        if came_from == login_url:
            came_from = route_url('home', self.request)

        session = meta.Session()
        login = data.pop('login')
        password = data.pop('password')
        query = session.query(User)
        user = query.filter(User.username == login).first()\
            or query.filter(User.email == login).first()
        if user is not None and user.authenticate(password):
            log.info('%s login' % user.username)
            headers = remember(self.request, user.id)
            self.request.session.flash('Login Success!')
            return HTTPFound(location=came_from, headers=headers)
        else:
            self.form.errors.append('username or password error, please try \
                    again')
            return None

    def __call__(self):
        if self.request.user is not None:
            self.request.session.flash('You are already login')
            return HTTPFound(self.request.route_url('home'))
        if self.request.method == 'POST':
            response = self.do_post()
            if response is not None:
                return response
        return {'form': self.form}


@view_config(route_name='logout')
def logout(request):
    came_from = request.params.get('url', route_url('home', request))
    request.session.invalidate()
    request.session.flash('Logged out')
    headers = forget(request)
    return HTTPFound(location=came_from, headers=headers)


@view_config(route_name='home', renderer='home.html')
class Home(BasicView):

    def __call__(self):
        session = meta.Session()
        posts = session.query(Post)\
            .filter(Post.status == 'publish')\
            .order_by(Post.id.desc()).limit(15)
        photos = session.query(Photo)\
            .order_by(Photo.updated_at.desc()).limit(4)
        return {'posts': posts, 'photos': photos}


@view_config(route_name='all_photos', renderer='photos/all_photos.html')
@view_config(route_name='all_photos_pagination', renderer='photos/all_photos.html')
class AllAlbumsView(BasicView):

    batch_size = 20

    def __call__(self):
        page = int(self.request.matchdict.get('page', 0))
        batch_offset = page * self.batch_size
        photos = meta.Session.query(Photo)\
            .order_by(Photo.created_at.desc()).limit(self.batch_size).offset(batch_offset)
        return {'photos': photos, 'next': page + 1}


@view_config(route_name='about', renderer='about.html')
class AboutMeView(BasicView):

    def __call__(self):
        resume = RESUME_EN if self.request.locale_name == 'en' else RESUME_CN
        return {'resume': resume}
