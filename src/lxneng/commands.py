from paste.script.command import Command
import os.path
from pyramid.threadlocal import manager as threadlocal_manager
from paste.deploy import loadapp


class PyramidCommand(Command):

    group_name = "lxneng"
    min_args = 1
    max_args = 1
    parser = Command.standard_parser()

    def setupPyramid(self):
        app = loadapp('config:%s' % self.args[0],
                relative_to=os.path.abspath('.'))
        registry = app.registry
        threadlocal_manager.push({'registry': registry, 'request': None})


class DemoCommand(PyramidCommand):
    summary = "--NO SUMMARY--"
    usage = "paster --plugin=lxneng demo_script development.ini"
    parser = PyramidCommand.standard_parser()

    def command(self):
        from s4u.sqlalchemy import meta
        from lxneng.models import Post
        self.setupPyramid()
        print "Hello, app script world!"
        query = meta.Session.query(Post)
        for post in query:
            print post.post_title.encode('utf-8')


class SyncFlickr(PyramidCommand):
    summary = "download flickr image"
    usage = "paster --plugin=lxneng sync_flickr development.ini"
    parser = PyramidCommand.standard_parser()

    def command(self):
        from s4u.sqlalchemy import meta
        from pyramid.threadlocal import get_current_registry
        from lxneng.models.photo import Album
        from lxneng.models.photo import Photo
        import flickrapi
        import json
        import transaction
        import os
        import urllib2
        from datetime import datetime
        self.setupPyramid()

        user_id = '37212768@N05'
        key = 'e64d9c7e5823e5d7c00f156c69c13bd2'
        url_tmpl = "http://farm%s.static.flickr.com/%s/%s_%s_z.jpg"
        session = meta.Session()

        image_dir = get_current_registry().settings['photos_dir']

        flickr = flickrapi.FlickrAPI(key, format='json')
        photosets_list = flickr.photosets_getList(user_id=user_id)[14:-1]
        photosets_list_json = \
            json.loads(photosets_list)['photosets']['photoset']
        set_ids = []
        for pset in photosets_list_json:
            set_id = pset['id']
            set_ids.append(set_id)

            entry = session.query(Album)\
                    .filter(Album.flickr_set_id == set_id).first()
            if entry is not None:
                continue

            set_title = pset['title']['_content'].encode('utf8')
            set_description = pset['description']['_content'].encode('utf8')
            album = Album(title=set_title,
                    description=set_description,
                    flickr_set_id=set_id)
            session.add(album)
        transaction.get().commit()

        for set_id in set_ids:
            album = session.query(Album)\
                    .filter(Album.flickr_set_id == set_id).first()
            set_photos = flickr.photosets_getphotos(photoset_id=set_id)[14:-1]
            set_photos_json = json.loads(set_photos)['photoset']['photo']
            for photo in set_photos_json:
                entry = session.query(Photo)\
                        .filter(Photo.flickr_photo_id == photo['id']).first()
                if entry is not None:
                    continue

                album.updated_at = datetime.now()
                photo_dir = os.path.join(image_dir, str(album.id))
                if not os.path.isdir(photo_dir):
                    os.mkdir(photo_dir)
                photo_path = os.path.join(str(album.id),
                            '%s.jpg' % photo['id'])
                file_path = os.path.join(image_dir, photo_path)
                url = url_tmpl % (photo['farm'], photo['server'],
                        photo['id'], photo['secret'])
                img = urllib2.urlopen(url).read()
                f = open(file_path, 'wb')
                f.write(img)
                f.close()
                print photo['id']

                entry = Photo(path=photo_path,
                        description=photo['title'].encode('utf8'),
                        is_primary=photo['isprimary'],
                        flickr_photo_id=photo['id'],
                        album_id=album.id)
                session.add(entry)
        transaction.get().commit()
