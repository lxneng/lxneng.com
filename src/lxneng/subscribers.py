from pyramid.events import subscriber
from pyramid.events import BeforeRender
from lxneng.utils import Tools

@subscriber(BeforeRender)
def add_renderer_globals(event):
    event['tools'] = Tools(event['request'])