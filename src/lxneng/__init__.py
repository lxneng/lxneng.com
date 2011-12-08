class HttpMethodOverrideMiddleware(object):
    """WSGI middleware for overriding HTTP Request Method for RESTful support
    """
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        if 'POST' == environ['REQUEST_METHOD']:
            override_method = ''

            # First check the '_method' form parameter
            if 'form-urlencoded' in environ['CONTENT_TYPE']:
                from webob import Request
                request = Request(environ)
                override_method = request.POST.get('_method', '').upper()

            # If not found, then look for 'X-HTTP-Method-Override' header
            if not override_method:
                override_method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE',
                                        '').upper()

            if override_method in ('PUT', 'DELETE', 'OPTIONS', 'PATCH'):
                # Save the original HTTP method
                environ['http_method_override.original_method'] =\
                        environ['REQUEST_METHOD']
                # Override HTTP method
                environ['REQUEST_METHOD'] = override_method

        return self.application(environ, start_response)


class ApplicationFactory(object):
    def create_configuration(self, settings):
        from pyramid.config import Configurator
        from pyramid.authentication import AuthTktAuthenticationPolicy
        from pyramid.authorization import ACLAuthorizationPolicy
        from pyramid_beaker import session_factory_from_settings
        from pyramid_beaker import set_cache_regions_from_settings
        from lxneng.factories import RootFactory

        set_cache_regions_from_settings(settings)

        config = Configurator(settings=settings,
                session_factory=session_factory_from_settings(settings),
                root_factory=RootFactory,
                authentication_policy=AuthTktAuthenticationPolicy('secret'),
                authorization_policy=ACLAuthorizationPolicy()
            )
        return config

    def setup_sqlalchemy(self, config):
        from s4u.sqlalchemy import includeme
        includeme(config)

    def setup_jinja2(self, config):
        from pyramid_jinja2 import renderer_factory
        config.add_translation_dirs('lxneng:locale')
        config.add_renderer('.html', renderer_factory)

    def setup_routes(self, config, settings):
        from lxneng import factories
        config.add_static_view('static', 'lxneng:static', cache_max_age=3600)
        config.add_static_view('static_photos', settings['photos_dir'],
                cache_max_age=3600)
        config.add_route('home', '/')
        config.add_route('login', '/login')
        config.add_route('logout', '/logout')
        config.add_route('about', '/about')
        config.add_route('photos', '/photos')
        config.add_route('photos_album', '/photos/albums/{id:\d+}',
                factory=factories.AlbumFactory)
        config.add_route('posts_index', '/posts')
        config.add_route('posts_new', '/posts/new')
        config.add_route('posts_tags_index', '/posts/tags')
        config.add_route('posts_rss', '/posts/rss')
        config.add_route('posts_show', '/posts/{id:\d+}',
                factory=factories.PostFactory)
        config.add_route('posts_edit', '/posts/{id:\d+}/edit',\
                factory=factories.PostFactory)
        config.add_route('posts_delete', '/posts/{id:\d+}/delete')
        config.add_route('posts_tags_show', '/posts/tags/{name}',
                factory=factories.tag_factory)

    def setup_assetviews(self, config):
        config.include('pyramid_assetviews')
        config.add_asset_views('lxneng:static', filenames=['robots.txt',
            'favicon.ico'], http_cache=5000)

    def configure(self, settings):
        config = self.create_configuration(settings)
        self.setup_sqlalchemy(config)
        self.setup_jinja2(config)
        self.setup_routes(config, settings)
        self.setup_assetviews(config)
        config.scan()
        return config

    def __call__(self, global_config, **settings):
        config = self.configure(settings)
        app = config.make_wsgi_app()
        return HttpMethodOverrideMiddleware(app)


app_factory = ApplicationFactory()


def main(global_config, **settings):
    return app_factory(global_config, **settings)
