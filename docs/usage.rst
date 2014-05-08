#########################
Working with django_dbdev
#########################


********************
Create your database
********************

To setup an isolated database environment with a development database and user in the ``dbdev_tempdata/<dbengine>/`` directory, run::

    $ python manage.py dbdev_init

After running this, you should be able to initialize the database using ``syncdb``::

    $ python manage.py syncdb

.. note::

    If you do not want to use ``dbdev_tempdata/`` as the data directory,
    simply set the ``DBDEV_DATADIR``-setting (in your settings.py) to
    something else.

.. note::

    If ``dbdev_init`` fails, read the output to determine what went wrong.
    Then run ``debdev_destroy`` (explained below) to remove everything that
    ``dbdev_init`` created before you try again.



*******************************************
Destroy or re-init the database environment
*******************************************
You can destroy your development database and all of the files associated with it except for backups using::

    $ python manage.py dbdev_destroy

We also provide a shortcut that is equivalent to running ``dbdev_destroy`` followed by ``dbdev_init``::

    $ python manage.py dbdev_reinit


********************
Load a database dump
********************
You can load a database dump using::

    $ python manage.py dbdev_loaddump /path/to/dumpfile.sql



*************
Make a backup
*************
You can dump your current database into::

    $ python manage.py dbdev_loaddump /path/to/dumpfile.sql


*************************
Start your database shell
*************************
Logging into your database shell is provided by the standard Django management command ``dbshell``::

    $ python manage.py dbshell