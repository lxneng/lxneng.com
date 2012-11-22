import os
import re
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            # TODO support version numbers
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links


requires = parse_requirements('requirements.txt')

setup(name='lxneng',
      version='1.1',
      description='lxneng',
      long_description=README + '\n\n' + CHANGES,
      author='Eric Lo',
      author_email='lxneng@gmail.com',
      url='http://lxneng.com',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      dependency_links=parse_dependency_links('requirements.txt'),
      tests_require=requires,
      test_suite="lxneng",
      message_extractors={'src': [
                          ('**.py', 'lingua_python', None),
     ('**.html', 'lingua_jinja2', None),
      ]},
      entry_points="""\
      [paste.app_factory]
      main = lxneng:main

      [console_scripts]
      sync_flickr = lxneng.commands.sync_flickr:main
      """,
      )
