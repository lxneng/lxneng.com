import logging
from itertools import groupby
from s4u.sqlalchemy import meta
from pyramid.view import view_config
from pyramid.response import Response
from lxneng.models.post import Post
from lxneng.models.post import Tag
from lxneng.views import BasicFormView
from lxneng.utils import markdown2html
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from flatland import Form, String
import webhelpers.feedgenerator as feedgenerator
from beaker.cache import cache_region

log = logging.getLogger(__name__)


class PostForm(Form):
    title = String
    content = String
    tags_string = String


class PostView(BasicFormView):

    form_class = PostForm

    @view_config(route_name='posts_index', renderer='posts/index.html')
    def index(self):
        def grouper(item):
            return item.created_at.year, item.created_at.month

        posts = meta.Session.query(Post)\
                .order_by(Post.id.desc()).all()
        result = groupby(posts, grouper)
        return {'result': result}

    def _cachekey(self):
        return (self.request.application_url, str(self.context.id))

    @cache_region('long_term', _cachekey)
    @view_config(route_name='posts_show', renderer='posts/show.html')
    def show(self):
        session = meta.Session()
        prev = session.query(Post).filter(Post.id < self.context.id)\
                .order_by(Post.id.desc()).first()
        next = session.query(Post).filter(Post.id > self.context.id)\
                .order_by(Post.id).first()
        return {'context': self.context, 'prev': prev, 'next': next}

    @view_config(route_name='posts_new', permission='auth',
            renderer='posts/edit.html')
    def add(self):
        if self.request.method == 'POST':
            data = self.form.value
            tags = Tag.create_tags(data.pop('tags_string'))
            entry = Post(**data)
            entry.tags = tags
            meta.Session.add(entry)
            return HTTPFound(route_url('posts_index', self.request))
        return {'form': self.form, 'title': 'Create Post'}

    @view_config(route_name='posts_edit', permission='auth',
            renderer='posts/edit.html')
    def edit(self):
        if self.request.method == 'POST':
            data = self.form.value
            tags = Tag.create_tags(data.pop('tags_string'))
            self.context.tags = tags
            for k, v in data.items():
                setattr(self.context, k, v)
            return HTTPFound(route_url('posts_show', id=self.context.id,
                request=self.request))
        self.form['tags_string'] = self.context.tags_string
        return {'form': self.form, 'title': 'Edit Post'}

    @view_config(route_name='posts_delete', request_method='DELETE',
            permission='auth')
    def destory(self):
        return HTTPFound(route_url('posts_index', self.request))

    @cache_region('long_term')
    @view_config(route_name='posts_tags_index',
            renderer='posts/tags/index.html')
    def tags_index(self):
        tags = Tag.tag_counts()
        return {'tags': tags}

    @cache_region('moderate_term')
    @view_config(route_name='posts_rss')
    def rss(self):
        posts = meta.Session.query(Post)\
                .order_by(Post.id.desc()).limit(20)
        feed = feedgenerator.Rss201rev2Feed(
                title="Hi, I'm Eric",
                link='http://lxneng.com',
                description="Eric's Thoughts and Writings")
        for post in posts:
            feed.add_item(title=post.title, link=route_url('posts_show',
                id=post.id, request=self.request),
                description=markdown2html(post.content))
        return Response(content_type='application/atom+xml',
                body=feed.writeString('utf-8'))
