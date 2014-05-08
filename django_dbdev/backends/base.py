from datetime import datetime
import os
from shutil import rmtree
from django.conf import settings


class BaseDbdevBackend(object):

    def __init__(self, command):
        """
        :param command:
            A Django management command class. Will always be a
            subclass of ``django_dbdev.management.commands._base.BaseDbdevCommand``.
        """
        self.command = command


    #####################################################
    #
    # The API each backend needs to implement.
    #
    #####################################################

    def init(self):
        """
        Create the database and grant the required previleges to
        the database user.
        """
        raise NotImplementedError()

    def destroy(self):
        """
        Remove all the files for the database.

        Typically stops any running database server and deletes
        the data directory.
        """
        raise NotImplementedError()

    def run_database_server_in_foreground(self):
        """
        Run database server in the foreground.
        """
        raise NotImplementedError()

    def start_database_server(self):
        """
        Start database server in the background.
        """
        raise NotImplementedError()

    def stop_database_server(self):
        """
        Stop database server started with :meth:`.start_database_server`.
        """
        raise NotImplementedError()


    #####################################################
    #
    # Helper methods
    #
    #####################################################

    def backupdir(self):
        """
        Get the path to the backup directory for this database backend.
        """
        return os.path.join(self._root_datadir_path, self.dbengine)

    def create_timestamped_backupdir(self):
        """
        Create a timestamped directory within :meth:`.backupdir`.

        :return: The path to the created directory.
        """
        return datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')

    @property
    def datadir(self):
        """
        Get the path to the temporary data directory for this database backend.

        The directory is created if it does not exist.
        """
        return os.path.join(self._root_datadir_path, self.__class__.__name__)

    @property
    def _root_datadir_path(self):
        return getattr(settings, 'DBDEV_DATADIR', 'dbdev_tempdata')

    def create_datadir_if_not_exists(self):
        """
        Create :meth:`.datadir` if it does not exist.
        """
        if not os.path.exists(self.datadir):
            os.makedirs(self.datadir)

    def remove_datadir(self):
        """
        Remove the :meth:`.datadir`.
        """
        rmtree(self.datadir)


    @property
    def stdout(self):
        """
        Shortcut for ``self.command.stdout``.

        Use for normal messages. I.E.::

            self.stdout.write('Something useful here!')
        """
        return self.command.stdout

    @property
    def stderr(self):
        """
        Shortcut for ``self.command.stderr``.

        Use for error messages. I.E.::

            self.stderr.write('An error of some sort')
        """
        return self.command.stderr