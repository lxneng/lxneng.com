from pyramid.config import Configurator
from pyramid_jinja2 import renderer_factory
from s4u.sqlalchemy import includeme
from lxneng import factories
from pyramid_beaker import session_factory_from_settings

def main(global_config, **settings):
    config = Configurator(settings=settings)
    includeme(config)
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
    config.add_translation_dirs('lxneng:locale')
    config.add_renderer('.html', renderer_factory)
    config.add_static_view('static', 'lxneng:static', cache_max_age=3600)
    config.add_route("home", "/")
    config.add_route("about", "/about")
    config.add_route("blog", "/blog")
    config.add_route("post", "/posts/:id", factory=factories.PostFactory)
    config.scan()
    return config.make_wsgi_app()
