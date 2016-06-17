Debug server errors
===================
- The server log is in {{backend.serverlogfile}}.


Work with the psql shell
========================
You should normally do this using the ``dbshell`` Django management command, but
if you need to add custom command line arguments or pipe data, take a look a
these examples.

Connect to the database in the psql shell (same as ``manage.py dbshell``)::

    $ {{backend.psql}} {{ dbsettings.NAME }}

Load a database dump (just like the dbdev_loaddump management command)::

    $ {{backend.psql}} {{ dbsettings.NAME }} < mydump.sql


.. note::
    You do not need any login info because we create and run the server
    as your local user.


Importing heroku backups
========================

Create a backup::

    $ curl -o latest.dump `heroku pg:backups public-url --app myapp`

Load the backup into your dbdev database::

    $ python manage.py dbdev_reinit
    $ python manage.py dbdev_loaddump latest.dump
