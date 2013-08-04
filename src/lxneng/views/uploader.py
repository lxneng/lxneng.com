import os
from pyramid.view import view_config
from lxneng.views import BasicView


@view_config(route_name='uploader',
             permission='auth',
             renderer='uploader.html')
class Upyun(BasicView):

    def do_post(self):
        data = self.request.POST
        image = data['image']
        images_dir = self.request.registry.settings.get('images_dir', '/tmp')
        if image != u'':
            path = os.path.join(images_dir, image.filename)
            with open(path, 'wb') as f:
                f.write(image.file.read())
            self.request.session['last_upload'] = path

    def __call__(self):
        if self.request.method == 'POST':
            self.do_post()
        return {}
