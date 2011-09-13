import os
from paste.deploy import loadapp
from paste.httpserver import serve

here = os.path.abspath(os.path.dirname(__file__))
config_file_path = os.path.join(here, 'development.ini')
application = loadapp('config:%s' % config_file_path)
