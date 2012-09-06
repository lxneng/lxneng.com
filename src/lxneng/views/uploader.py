from pyramid.view import view_config
from lxneng.views import BasicView


@view_config(route_name='uploader', renderer='uploader.html')
class Upyun(BasicView):

    def __init__(self, context, request):
        super(Upyun, self).__init__(context, request)
        self.upyun = request.registry['upyun']
        self.upyun.set_bucket('lxneng')

    def do_post(self):
        data = self.request.POST
        image = data['image']
        if image != u'':
            path = '/images/%s' % image.filename
            rt = self.upyun.writeFile(path, image.file)
            if rt:
                self.request.session['last_upload'] = path

    def __call__(self):
        if self.request.method == 'POST':
            self.do_post()
        return {}
