from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.events import NewRequest
from flatland.out.markup import Generator
from pyramid.httpexceptions import HTTPForbidden
from lxneng.utils import Tools
from lxneng.factories import get_user


@subscriber(BeforeRender)
def add_renderer_globals(event):
    event['tools'] = Tools(event['request'])
    event['html'] = Generator()
    event['user'] = get_user(event['request'])


@subscriber(NewRequest)
def csrf_validation(event):
    if event.request.method == 'POST':
        token = event.request.POST.get('_csrf')
        if token is None or token != event.request.session.get_csrf_token():
            raise HTTPForbidden('CSRF token is missing or invalid')
