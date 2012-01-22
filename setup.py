import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'repoze.tm2>=1.0b1', # default_commit_veto
    'sqlalchemy',
    'zope.sqlalchemy',
    'WebError',
    'psycopg2',
    'httplib2',
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='defpage.security',
      version='0.1',
      description='defpage authentication and registration service',
      long_description=README + '\n\n' +  CHANGES,
      packages=find_packages(),
      namespace_packages=['defpage'],
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require = requires,
      test_suite="defpage.security",
      entry_points = """\
      [paste.app_factory]
      main = defpage.security:main
      """,
      paster_plugins=['pyramid'],
      )
