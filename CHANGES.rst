Oct. 15, 2011
---------------

- sync flickr photos


Oct. 14, 2011
---------------

- add fabric config file
- add paster command template
- modify login view
- modify event
- modify PO file
- add models Album, Photo, and using s4u.image for image scale

Oct. 10, 2011
---------------

- fix config error 


Sept. 28, 2011
---------------

- add user Model 
- add HTTPForbidden page
- add login page
- db migration script
- using py-bcrypt for password hashing
- Authentication settings
- add RootFactory for auth

Sept. 27, 2011
---------------

- fix MANIFEST.ini file
- using s4u.upgrade for migration 
    ``upgrade --scan lxneng --db-uri mysql://root@localhost/lxneng``

Sept. 26, 2011
---------------

- using pyramid_beaker for cache


Sept. 23, 2011
---------------

- markdown the post content

- using pygments for code syntax hightlight 

Sept. 22, 2011
---------------

- add photos page

- store locale_name in session

- using pyramid_beaker as session factory

- add bio page 

- using supervisor control gunicorn_paster
  ``supervisorctl restart gunicorn``
  
Sept. 19, 2011
---------------

- add Post detail page 
  
Sept. 17, 2011
---------------

- Home page slideshow 

Sept. 14, 2011
---------------

- add charset to sqlalchemy.url 

Sept. 14, 2011
---------------

- modify layout

Sept. 11, 2011
---------------

- add BaseView 

- setup i18n and design new layout

Sept. 10, 2011
---------------

- add sqlalchemy logger

- fix reduplicate function name

Sept. 9, 2011
---------------

- add requirements.txt, support ``pip install -r requirements.txt`` and setup.py

Sept. 8, 2011
---------------

- using s4u.sqlalchemy

- init sqlalchemy

- Serving favicon.ico from the root

- Serving robots.txt from the root

- Initial version
