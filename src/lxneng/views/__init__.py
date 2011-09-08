from pyramid.view import view_config


@view_config(context='pyramid.exceptions.NotFound', renderer='404.html')
@view_config(route_name='home', renderer='home.html')
def static_view(request):
    return {'name': 'Eric'}
