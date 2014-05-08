import os
from sh import Command
from sh import ErrorReturnCode
from django.conf import settings

from .base import BaseDbdevBackend


DBSETTINGS = {
    'ENGINE':'django.db.backends.mysql',
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
        self.common_command_kwargs = dict(
            _out=self.stdout,
            _err=self.stderr,
            _out_bufsize=1)
        self.mysqld = Command(mysqld_executable).bake(
            datadir=os.path.abspath(self.datadir),
            port=DBSETTINGS['PORT'],
            **self.common_command_kwargs)
        self.mysqladmin = Command(mysqladmin_executable).bake(
            port=DBSETTINGS['PORT'],
            user=DBSETTINGS['USER'],
            password=DBSETTINGS['PASSWORD'],
            **self.common_command_kwargs)
        self.mysqladmin_nopassword = Command(mysqladmin_executable).bake(
            port=DBSETTINGS['PORT'],
            user=DBSETTINGS['USER'],
            **self.common_command_kwargs)

        self.mysql_basedir = os.environ.get('DBDEV_MYSQL_BASEDIR',
            getattr(settings, 'DBDEV_MYSQL_BASEDIR', None))
        mysql_install_db_kwargs = self.common_command_kwargs.copy()
        if self.mysql_basedir:
            mysql_install_db_kwargs['basedir'] = self.mysql_basedir
        self.mysql_install_db = Command(mysql_install_db_executable).bake(
            datadir=os.path.abspath(self.datadir),
            **mysql_install_db_kwargs)

    def mysqlserver(self, *args):
        mysqlserver_executable = getattr(settings, 'DBDEV_MYSQLSERVER_EXECUTABLE', 'mysql.server')
        allargs = list(args) + [
            '--datadir', os.path.abspath(self.datadir),
            # '--pidfile', os.path.abspath(os.path.join(self.datadir, 'pidfile.pid'))
        ]
        if self.mysql_basedir:
            allargs.append('--basedir')
            allargs.append(self.mysql_basedir)

        # NOTE: Does not work because we have no way of setting the port.
        mysqlserver = Command(mysqlserver_executable).bake(*allargs,
            _out=self.stdout,
            _err=self.stderr,
            _out_bufsize=0)
        self.stdout.write('Running: {}'.format(mysqlserver))
        return mysqlserver()
        

    def start_database_server(self):
        self.mysqlserver('start')

    def _stop_database_server(self):
        self.mysqlserver('stop')

    def stop_database_server(self):
        try:
            self._stop_database_server()
        except ErrorReturnCode:
            pass # The error message from mysqladmin is shown to the user, so no more is needed from us

    def _set_password_for_rootuser(self):
        self.mysqladmin_nopassword('password', DBSETTINGS['PASSWORD'])

    def _create_database(self):
        self.mysqladmin_nopassword('create', DBSETTINGS['NAME'])

    def init(self):
        if os.path.exists(self.datadir):
            self.stderr.write('The data directory ({}) already exists.'.format(self.datadir))
            raise SystemExit()
        else:
            self.create_datadir_if_not_exists()
            self.mysql_install_db()
            self.start_database_server()
            self._set_password_for_rootuser()
            self._create_database()

            # self.stdout.write('')
            # self.stdout.write('='*70)
            # self.stdout.write('')
            # self.stdout.write('Successfully:')
            # self.stdout.write('- Initialized postgres in "{}".'.format(self.datadir))
            # self.stdout.write('- Created the "{USER}"-role with password'.format(**DBSETTINGS))
            # self.stdout.write('  "{PASSWORD}" and superuser previleges'.format(**DBSETTINGS))
            # self.stdout.write('- Created an empty database named "{NAME}".'.format(**DBSETTINGS))
            # self.stdout.write('')
            # self.stdout.write('The postgres server is running on port {PORT}.'.format(**DBSETTINGS))
            # self.stdout.write('You can stop it with:')
            # self.stdout.write('')
            # self.stdout.write('  $ python manage.py dbdev_stopserver')
            # self.stdout.write('')
            # self.stdout.write('='*70)

    def destroy(self):
        # self.stop_database_server()
        if os.path.exists(self.datadir):
            self.remove_datadir()
            self.stdout.write('Successfully stopped the MySQL server and removed "{}".'.format(
                self.datadir))