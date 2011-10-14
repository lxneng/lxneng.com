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
        app = loadapp('config:%s' % self.args[0], relative_to=os.path.abspath('.'))
        registry = app.registry
        try:
            threadlocal_manager.push({'registry':registry})
        finally:
            threadlocal_manager.pop()


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
