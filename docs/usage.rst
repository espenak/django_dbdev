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


******************
Backup and restore
******************
You can dump your current database into ``dbdev_tempdata/<backend>-backups/`` with::

    $ python manage.py dbdev_backup

And you can restore the last backup using::

    $ python manage.py dbdev_restore

.. warning::

    When you restore a backup, ``dbdev_restore`` runs ``dbdev_reinit`` to
    ensure you restore to a clean database enviroment. This means that you
    will loose all data on the server when you restore a backup, uncluding
    any extra database you may have added.

You can list all backups with::

    $ python manage.py dbdev_listbackups

And restore a backup by name with::

    $ python manage.py dbdev_restore <path-to-backupdir>

If you make a more important backup, you can use a name for it::

    $ python manage.py dbdev_backup -n mybackup
    ... and restore with
    $ python manage.py dbdev_restore -n mybackup

Backup names are unique, so you will not be able to create multiple backups with
the same name.

Finally, you can clear all backups for your backend using::

    $ python manage.py dbdev_clearbackups

.. note::
    ``dbdev_destroy`` and ``dbdev_reinit`` does not affect backups.


*************************
Start your database shell
*************************
Logging into your database shell is provided by the standard Django management command ``dbshell``::

    $ python manage.py dbshell


****************************************************************
Help remembering all those database debugging comands and quirks
****************************************************************
Each backend provides a guide with tips and examples. Run::

    $ python manage.py dbdev_guide

To show this guide.