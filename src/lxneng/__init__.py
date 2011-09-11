from pyramid.config import Configurator
from pyramid_jinja2 import renderer_factory
from s4u.sqlalchemy import includeme


def main(global_config, **settings):
    settings = dict(settings)
    settings.setdefault('jinja2.i18n.domain', 'lxneng')
    config = Configurator(settings=settings)
    includeme(config)
    config.add_translation_dirs('locale/')
    config.add_renderer('.html', renderer_factory)
    config.add_static_view('static', 'lxneng:static', cache_max_age=3600)
    config.add_route("home", "/")
    config.scan()
    return config.make_wsgi_app()
