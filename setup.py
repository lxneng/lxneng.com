import os
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

version = '1.0'
requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'SQLAlchemy',
    'zope.sqlalchemy',
    's4u.sqlalchemy',
    ]

setup(name='lxneng',
      version=version,
      description='lxneng',
      long_description=README + '\n\n' + CHANGES,
      author='Eric Lo',
      author_email='lxneng@gmail.com',
      url='http://lxneng.com',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=["lxneng"],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="lxneng",
      entry_points="""\
      [paste.app_factory]
      main = lxneng:main
      """,
      paster_plugins=['pyramid'],
      )
