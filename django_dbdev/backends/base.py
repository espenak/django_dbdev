from datetime import datetime
import os
import importlib
from shutil import rmtree

from builtins import object
from django.conf import settings
from django.template.loader import render_to_string


class BaseDbdevBackend(object):
    """
    Abstract base class for dbdev backends.
    """

    def __init__(self, command):
        """
        :param command: A Django management command class. Will always be a subclass of ``django_dbdev.management.commands._base.BaseDbdevCommand``.
        """
        self.command = command

    @property
    def dbsettings(self):
        return settings.DATABASES['default']

    def sh_stdout_handler(self, data):
        return self.stdout.write(data)

    def sh_stderr_handler(self, data):
        return self.stderr.write(data)

    #####################################################
    #
    # The API each backend needs to implement.
    # In addition to these methods, a backend must also:
    # - Add a DBSETTINGS dict to the backend module
    #   (see the other backends).
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

    def backup(self, directory):
        """
        Create a backup of the database.

        :param directory: The backup directory to create the backup in.
        """
        raise NotImplementedError()

    def restore(self, directory):
        """
        Restore a backup created with :meth:`.backup.`

        :param directory: The backup directory to restore.
        """
        raise NotImplementedError()

    def serverinfo(self):
        """
        Print information about the server.

        Must at least tell if the server is running or not.
        """
        raise NotImplementedError()

    def guide(self):
        """
        Print useful database specific commands and tips for the user.

        Examples should include all the needed login info.

        The idea is to avoid having to lookup those commonly needed
        database-specific management and connection commands that
        is needed from time to time.

        The default expects the backend to create a Django template
        named ``django_dbdev/<backend-class-name-lowercased>.rst``.
        The template gets the backend class as ``backend`` context
        variable, and the ``dbsettings`` context variable contains
        ``<backendmodule>.DBSETTINGS``.

        Use the ReStructuredText format for the text.
        """
        return render_to_string('django_dbdev/{}.rst'.format(self.__class__.__name__.lower()), {
            'backend': self,
            'dbsettings': importlib.import_module(self.__class__.__module__).DBSETTINGS
        })

    #####################################################
    #
    # Helper methods
    #
    #####################################################

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

    @property
    def root_backupdir(self):
        """
        Get the path to the backup directory for this database backend.
        """
        return os.path.join(self._root_datadir_path, '{}-backups'.format(self.__class__.__name__))

    def create_timestamped_backupdir(self, name=None):
        """
        Create a timestamped directory within :meth:`.root_backupdir`.

        :return: The path to the created directory.
        """
        dirname = datetime.now().strftime('backup-%Y-%m-%d_%H-%M-%S-%f')
        if name:
            dirname = '{}.{}'.format(dirname, name)
        dirpath = os.path.join(self.root_backupdir, dirname)
        os.makedirs(dirpath)
        return dirpath

    def get_backupdirs(self):
        if os.path.exists(self.root_backupdir):
            return [d for d in os.listdir(self.root_backupdir) if d.startswith('backup-')]
        else:
            return []

    def _get_backupdirs_sorted_descending(self):
        backupdirs = self.get_backupdirs()
        backupdirs.sort()
        backupdirs.reverse()
        backupdirs = [os.path.join(self.root_backupdir, backupdir) for backupdir in backupdirs]
        return backupdirs

    def get_last_backupdir(self):
        return self._get_backupdirs_sorted_descending()[0]

    def find_named_backupdir(self, name):
        backupdirs = self.get_backupdirs()
        suffix = '.{}'.format(name)
        for directory in backupdirs:
            if directory.endswith(suffix):
                return os.path.join(self.root_backupdir, directory)
        return None

    def reinit(self):
        """
        Destroy and re-initialize.
        """
        self.destroy()
        self.init()
