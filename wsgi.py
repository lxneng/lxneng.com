import sys
from paste.deploy import loadapp
from paste.httpserver import serve


if __name__ == '__main__':
    serve(loadapp('config:/Users/eric/Projects/lxneng/development.ini'), host='0.0.0.0', port=8088) 
else:
    sys.path.append('/home/dotcloud/code')
    application = loadapp('config:/home/dotcloud/code/development.ini')

