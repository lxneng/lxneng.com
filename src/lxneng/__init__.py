from pyramid.config import Configurator
from pyramid_jinja2 import renderer_factory


def main(global_config, **settings):
    from sqlalchemy import engine_from_config
    from lxneng.models import init_sqlalchemy
    engine = engine_from_config(settings, 'sqlalchemy.')
    init_sqlalchemy(engine)
    config = Configurator(settings=settings)
    config.add_renderer('.html', renderer_factory)
    config.add_static_view('static', 'lxneng:static', cache_max_age=3600)
    config.add_route("home", "/")
    config.scan()
    return config.make_wsgi_app()
