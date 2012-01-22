===========================
defpage.com security server
===========================

Create PostgreSQL database
-------------------------

Create user `defpage`, database `defpage` and make him owner::

  # su - postgres
  $ createuser -lsWRD defpage_security
  (see password in .ini file)
  $ createdb defpage_security
  $ echo "alter database defpage_security owner to defpage_security;" | psql defpage_security

Deploy
======

Create virtual environment and deploy server within it::

  $ git clone git@spacta.com:defpage/security.git
  $ cd defpage_security
  $ virtualenv --no-site-packages --distribute .
  $ bin/pip install -e .

Run tests::

  $ bin/python setup.py test

Run site for development::

  $ bin/pserve development.ini --reload

Run site in production::

  $ bin/pserve production.ini --daemon

Upgrading
=========

Apply sql pathces::

  $ psql -U defpage_security < sql/patch.sql

Build test services with NetCat
===============================

Simulate notifcation unit server with UNIX util netcat::

  $ echo -e "HTTP/1.1 202 Accepted\n" | nc -lp 9004 -q 1
