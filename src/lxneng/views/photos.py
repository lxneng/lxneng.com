from lxneng.views import BasicView
from lxneng.views import BasicFormView
from lxneng.models.photo import Album
from lxneng.models.photo import Photo
from flatland import Form
from flatland import String
from beaker.cache import cache_region
from pyramid.view import view_config
from easy_sqlalchemy import meta
from pyramid.httpexceptions import HTTPFound


class AlbumForm(Form):
    title = String
    description = String


class AlbumView(BasicFormView):

    form_class = AlbumForm

    @view_config(route_name='photos', renderer='photos/index.html')
    def index(self):

        @cache_region('long_term')
        def data():
            photos = Photo.query\
                .order_by(Photo.updated_at.desc())\
                .limit(10)
            albums = Album.query.order_by(Album.updated_at.desc())
            return {'photos': photos, 'albums': albums}
        return data()

    @view_config(route_name='photos_album', renderer='photos/album.html')
    def show(self):
        return {}

    @view_config(route_name='photos_album_new', renderer='photos/edit_album.html')
    def new(self):
        if self.request.method == 'POST':
            session = meta.Session()
            data = self.form.value
            entry = Album(**data)
            session.add(entry)
            session.flush()
            return HTTPFound(self.request.route_url('photos_album', id=entry.id))
        return {'form': self.form, 'title': 'Create Album'}

    @view_config(route_name='photos_album_edit',
                 renderer='photos/edit_album.html')
    def edit(self):
        if self.request.method == 'POST':
            data = self.form.value
            for k, v in data.items():
                setattr(self.context, k, v)
            return HTTPFound(self.request.route_url('photos_album', id=self.context.id))
        return {'form': self.form, 'title': 'Edit Album'}


class AlbumPhotoView(BasicView):

    def __init__(self, context, request):
        super(AlbumPhotoView, self).__init__(context, request)
        self.upyun = request.registry['upyun']
        self.upyun.set_bucket('lxneng')

    @view_config(route_name='photos_album_upload',
                 renderer='photos/upload_to_album.html')
    def upload(self):
        if self.request.method == 'POST':
            data = self.request.POST
            image = data['image']
            if image != u'':
                path = '%s/%s' % (self.context.id, image.filename)
            rt = self.upyun.writeFile('/photos/%s' % path, image.file, True)
            if rt:
                entry = Photo(album_id=self.context.id, path=path, description=data['description'])
                meta.Session.add(entry)
                return HTTPFound(self.request.route_url('photos_album', id=self.context.id))
        return {'title': 'upload photos'}
