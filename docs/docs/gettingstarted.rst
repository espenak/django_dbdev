###############
Getting started
###############


*******
Install
*******
::

    $ pip install django_dbdev


*****************************
Configure your Django project
*****************************
Add ``django_dbdev`` to ``INSTALLED_APPS``, and setup one of the database backends (below).


Setup for PostgreSQL
====================
Add the following to your Django settings::

    from django_dbdev.backends.postgres import DBSETTINGS

    DATABASES = {
        'default': DBSETTINGS
    }


Setup for MySQL
===============
Add the following to your Django settings::

    from django_dbdev.backends.mysql import DBSETTINGS

    DATABASES = {
        'default': DBSETTINGS
    }



*****************************************
Developing for multiple database backends
*****************************************
TODO