from pyramid.config import Configurator
from pyramid_jinja2 import renderer_factory
import s4u.sqlalchemy
import s4u.image
from lxneng import factories
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_beaker import session_factory_from_settings
from pyramid_beaker import set_cache_regions_from_settings

def main(global_config, **settings):
    set_cache_regions_from_settings(settings)
    config = Configurator(settings=settings,
            session_factory=session_factory_from_settings(settings),
            root_factory=factories.RootFactory,
            authentication_policy=AuthTktAuthenticationPolicy('secret'),
            authorization_policy=ACLAuthorizationPolicy()
    )
    s4u.sqlalchemy.includeme(config)
    s4u.image.includeme(config)
    config.add_translation_dirs('lxneng:locale')
    config.add_renderer('.html', renderer_factory)
    config.add_static_view('static', 'lxneng:static', cache_max_age=3600)
    config.add_route("home", "/")
    config.add_route("login", "/login")
    config.add_route("logout", "/logout")
    config.add_route("about", "/about")
    config.add_route("blog", "/blog")
    config.add_route("photos", "/photos")
    config.add_route("post", "/posts/:id", factory=factories.PostFactory)
    config.scan()
    return config.make_wsgi_app()
