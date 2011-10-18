import logging
from itertools import groupby
from s4u.sqlalchemy import meta
from pyramid.view import view_config
from lxneng.models import Post
from lxneng.views import BasicFormView
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from flatland import Form, String

log = logging.getLogger(__name__)



class PostForm(Form):
    title = String
    content = String

class PostView(BasicFormView):

    form_class = PostForm 

    @view_config(route_name='posts_index', renderer='posts/index.html')
    def index(self):
        def grouper(item):
            return item.created_at.year, item.created_at.month

        posts = meta.Session.query(Post)\
                .filter(Post.status == 'publish')\
                .order_by(Post.id.desc()).all()
        result = groupby(posts, grouper)
        return {'result': result}

    
    @view_config(route_name='posts_show', renderer='posts/show.html')
    def show(self):
        return {'context': self.context}

    @view_config(route_name='posts_new', permission='auth',
            renderer='posts/edit.html')
    def add(self):
        if self.request.method == 'POST':
            data = self.form.value
            entry = Post(**data)
            meta.Session.add(entry)
            return HTTPFound(route_url('posts_index', self.request)) 
        return {'form': self.form, 'title': 'Create Post'}

    @view_config(route_name='posts_edit', permission='auth',
            renderer='posts/edit.html')
    def edit(self):
        if self.request.method == 'POST':
            data = self.form.value
            for k, v in data.items():
                setattr(self.context, k, v)
        return {'form': self.form, 'title': 'Edit Post'}

    @view_config(route_name='posts_delete', request_method='DELETE',
            permission='auth')
    def destory(self):
        return HTTPFound(route_url('posts_index', self.request)) 
