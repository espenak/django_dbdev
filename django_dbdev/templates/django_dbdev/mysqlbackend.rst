Debug server errors
===================
- The error log is in {{backend.errorlogfile}}.
- mysqladmin (see "Work with mysqladmin" below) is very useful when debugging.


MariaDB specific stuff
======================
With MaraiaDB, you can get a lot of debug information with the
``extended-status`` subcommand for ``mysqladmin``.


Work with the mysql shell
=========================
You should normally do this using the ``dbshell`` Django management command, but
if you need to add custom command line arguments or pipe data, take a look a
these examples.

Connect to the database in the mysql shell (same as ``manage.py dbshell``)::

    $ {{backend.mysql}} {{ dbsettings.NAME }}

Connect to the shell without selecting a database::

    $ {{backend.mysql}}

Load a database dump (just like the dbdev_loaddump management command)::

    $ {{backend.mysql}} {{ dbsettings.NAME }} < mydump.sql


Work with mysqld
================

.. note::
    Use should usually use ``mysqld_safe`` instead of ``mysqld``, so we use that
    for the examples below.

.. note::
    The MySQL commands are **very** bad at handling relative paths, so all the
    examples use absolute paths.


Start the server (same as the dbdev_startserver management command)::

    $ {{backend.mysqld}}

Use ``&`` to start the server in the background. In any case, you will have to
use *mysqladmin* or our Django management command to stop/shutdown the server.
It does not stop when you hit ``CTRL-C``.

.. note::
    The ``dbdev_fgrunserver`` management command starts mysqld in the
    foreground, but handles this ``CTRL-C`` issue, so you are probably better
    off using the management command.


Work with mysqldump
===================

Take a dump of the database::

    $ {{backend.mysqldump}} {{dbsettings.NAME}}


Work with mysqladmin
====================

See all available mysqladmin subcommands::

    $ {{backend.mysqladmin}}

Shutdown a running server (same as the dbdev_stopserver management command)::

    $ {{backend.mysqladmin}} shutdown

Enable debug logging (for the server log)::

    $ {{backend.mysqladmin}} debug

Create a new database named ``mydb``::

    $ {{backend.mysqladmin}} create mydb


Check if the MySQL server is running::

    $ {{backend.mysqladmin}} ping

See information about the running MySQL server::

    $ {{backend.mysqladmin}} status