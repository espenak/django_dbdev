.. django_dbdev documentation master file, created by
   sphinx-quickstart on Wed May  7 22:37:51 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django_dbdev's documentation!
========================================

**django_dbdev** is a set of Django management commands that makes it very easy work with database servers during development.

We provide Django management commands to:

- Setup a clean and isolated database environment in a temporary folder. This
  means that you do not have to touch ANY globally installed database configs or
  databases.
- Create and destroy this isolated database enviroment, including all those hard
  to remember commands to create the database, create a user with the correct
  privileges etc.
- Load database dumps.
- Backup and restore your database.


Supported databases
===================
- PostgreSQL
- MySQL
- MariaDB (same backend as MySQL)

You can also easily :doc:`add support for more databases <custom_backend>`.


Help
====

.. toctree::
   :maxdepth: 2

   gettingstarted
   usage
   settings
   custom_backend
   develop




Source and issues
=================
For sources and issue tracker, see the `GitHub page for the project
<https://github.com/espenak/django_dbdev>`_. If you plan to submit a patch,
please read :doc:`develop`.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

