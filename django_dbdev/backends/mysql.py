from future import standard_library
standard_library.install_aliases()
from io import StringIO
from time import sleep
import os
from sh import Command
from sh import ErrorReturnCode
from django.conf import settings

from .base import BaseDbdevBackend


DBSETTINGS = {
    'ENGINE': 'django.db.backends.mysql',
    'PORT': 20022,
    'NAME': 'dbdev',
    'USER': 'root',
    'PASSWORD': 'dbdev',
    'HOST': '127.0.0.1',
}


class MySqlBackend(BaseDbdevBackend):
    def __init__(self, command):
        super(MySqlBackend, self).__init__(command)
        mysql_install_db_executable = getattr(settings, 'DBDEV_MYSQL_INSTALL_DB_EXECUTABLE',
            'mysql_install_db')
        mysqld_executable = getattr(settings, 'DBDEV_MYSQLD_EXECUTABLE', 'mysqld_safe')
        mysqladmin_executable = getattr(settings, 'DBDEV_MYSQLADMIN_EXECUTABLE', 'mysqladmin')
        mysql_executable = getattr(settings, 'DBDEV_MYSQL_EXECUTABLE', 'mysql')
        mysqldump_executable = getattr(settings, 'DBDEV_MYSQLDUMP_EXECUTABLE', 'mysqldump')
        self.errorlogfile = os.path.join(self.datadir, 'servererror.log')
        self.common_command_kwargs = dict(
            _out=self.sh_stdout_handler,
            _err=self.sh_stderr_handler,
            _out_bufsize=1)
        self.mysqld = Command(mysqld_executable).bake(
            datadir=os.path.abspath(self.datadir),
            port=self.dbsettings['PORT'],
            log_error=os.path.abspath(self.errorlogfile),
            **self.common_command_kwargs)
        self.mysqladmin = Command(mysqladmin_executable).bake(
            port=self.dbsettings['PORT'],
            user=self.dbsettings['USER'],
            password=self.dbsettings['PASSWORD'],
            **self.common_command_kwargs)
        self.mysqladmin_nopassword = Command(mysqladmin_executable).bake(
            port=self.dbsettings['PORT'],
            user=self.dbsettings['USER'],
            **self.common_command_kwargs)
        self.mysql = Command(mysql_executable).bake(
            port=self.dbsettings['PORT'],
            user=self.dbsettings['USER'],
            password=self.dbsettings['PASSWORD'],
            **self.common_command_kwargs)
        self.mysqldump = Command(mysqldump_executable).bake(
            port=self.dbsettings['PORT'],
            user=self.dbsettings['USER'],
            password=self.dbsettings['PASSWORD'],
            **self.common_command_kwargs)

        self.mysql_basedir = os.environ.get('DBDEV_MYSQL_BASEDIR',
            getattr(settings, 'DBDEV_MYSQL_BASEDIR', None))
        mysql_install_db_kwargs = self.common_command_kwargs.copy()
        if self.mysql_basedir:
            mysql_install_db_kwargs['basedir'] = self.mysql_basedir
        self.mysql_install_db = Command(mysql_install_db_executable).bake(
            datadir=os.path.abspath(self.datadir),
            **mysql_install_db_kwargs)


    def _server_is_running(self, nopassword=False):
        output = StringIO()
        def process_output(line):
            output.write(line)
        try:
            if nopassword:
                p = self.mysqladmin_nopassword('ping', _out=process_output, _err=process_output)
            else:
                p = self.mysqladmin('ping', _out=process_output, _err=process_output)
            p.wait()
        except ErrorReturnCode:
            pass
        return 'mysqld is alive' in output.getvalue()
        
    def _wait_for_serverstart(self, nopassword=False):
        self.stdout.write('Waiting for MySQL server to start...')
        while not self._server_is_running(nopassword):
            self.stdout.write('... MySQL server not running. Re-pinging in 0.3s.')
            sleep(0.3)
        self.stdout.write('MySQL server is running.')

    def start_database_server(self, nopassword=False):
        if self._server_is_running(nopassword):
            self.stderr.write('MySQL server is already running.')
        else:
            self.mysqld(_bg=True)
            self._wait_for_serverstart(nopassword)

    def run_database_server_in_foreground(self):
        p = self.mysqld(_bg=True)
        try:
            p.wait()
        except KeyboardInterrupt:
            try:
                self._stop_database_server()
            except ErrorReturnCode:
                p.kill()


    def _stop_database_server(self):
        try:
            self.mysqladmin('shutdown')
        except ErrorReturnCode:
            self.stderr.write('Failed to stop MySQL server using:')
            self.stderr.write('   $ {} shutdown'.format(self.mysqladmin))
            self.stderr.write('Trying without password in case we have been left in a state where the root password was never set.')
            self.mysqladmin_nopassword('shutdown')
            self.stdout.write('Shutting down without password worked!')
        else:
            self.stdout.write('MySQL server was stopped.')

    def stop_database_server(self):
        try:
            self._stop_database_server()
        except ErrorReturnCode:
            pass

    def _set_password_for_rootuser(self):
        self.stdout.write('Setting MySQL server password for the root user to: "{PASSWORD}".'.format(
            **DBSETTINGS))
        self.mysqladmin_nopassword('password', self.dbsettings['PASSWORD'])

    def _create_database(self):
        self.stdout.write('Creating the "{NAME}"-database.'.format(**DBSETTINGS))
        self.mysqladmin('create', self.dbsettings['NAME'])

    def init(self):
        if os.path.exists(self.datadir):
            self.stderr.write('The data directory ({}) already exists.'.format(self.datadir))
            raise SystemExit()
        else:
            self.create_datadir_if_not_exists()
            self.mysql_install_db()
            self.start_database_server(nopassword=True)
            self._set_password_for_rootuser()
            self._create_database()

            self.stdout.write('')
            self.stdout.write('='*70)
            self.stdout.write('')
            self.stdout.write('Successfully:')
            self.stdout.write('- Initialized MySQL in "{}".'.format(self.datadir))
            self.stdout.write('- Created the "{USER}"-role with "{PASSWORD}" '.format(**DBSETTINGS))
            self.stdout.write('  as password and all previleges.')
            self.stdout.write('- Created an empty database named "{NAME}".'.format(**DBSETTINGS))
            self.stdout.write('')
            self.stdout.write('The MySQL server is running on port {PORT}.'.format(**DBSETTINGS))
            self.stdout.write('You can stop it with:')
            self.stdout.write('')
            self.stdout.write('  $ python manage.py dbdev_stopserver')
            self.stdout.write('')
            self.stdout.write('And you can shutdown and destroy the entire setup using:')
            self.stdout.write('')
            self.stdout.write('  $ python manage.py dbdev_destroy')
            self.stdout.write('')
            self.stdout.write('='*70)

    def destroy(self):
        self.stop_database_server()
        if os.path.exists(self.datadir):
            self.remove_datadir()
            self.stdout.write('Successfully stopped the MySQL server and removed "{}".'.format(
                self.datadir))

    def serverinfo(self):
        if self._server_is_running():
            self.mysqladmin('ping')
            self.mysqladmin('status')
        else:
            self.stdout.write('Server is not running.')

    def load_dbdump(self, dumpfile):
        with open(dumpfile, 'rb') as f:
            self.mysql(self.dbsettings['NAME'], _in=f)

    def backup(self, directory):
        backupfile = os.path.join(directory, 'backup.sql')
        with open(backupfile, 'wb') as f:
            self.mysqldump(self.dbsettings['NAME'], _out=f)

    def restore(self, directory):
        backupfile = os.path.join(directory, 'backup.sql')
        self.load_dbdump(backupfile)
