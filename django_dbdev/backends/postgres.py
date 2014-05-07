from sh import Command
from sh import ErrorReturnCode
import os.path
from django.conf import settings

from .base import BaseDbdevBackend

DBSETTINGS = {
    'ENGINE':'django.db.backends.postgresql_psycopg2',
    'PORT': 20021,
    'NAME': 'dbdev',
    'USER': 'dbdev',
    'PASSWORD': 'dbdev',
    'HOST': '127.0.0.1',
}


class PostgresBackend(BaseDbdevBackend):

    def __init__(self, command):
        self.command = command
        postgres_executable = getattr(settings, 'DBDEV_POSTGRES_EXECUTABLE', 'postgres')
        pg_ctl_executable = getattr(settings, 'DBDEV_POSTGRES_PG_CTL_EXECUTABLE', 'pg_ctl')
        psql_executable = getattr(settings, 'DBDEV_POSTGRES_PSQL_EXECUTABLE', 'psql')
        createdb_executable = getattr(settings, 'DBDEV_POSTGRES_CREATEDB_EXECUTABLE', 'createdb')
        environ = {
            'PGPORT': str(DBSETTINGS['PORT'])
        }
        common_command_kwargs = dict(
            _out=self.command.stdout,
            _err=self.command.stderr,
            _env=environ,
            _out_bufsize=1)
        self.postgres = Command(postgres_executable).bake(**common_command_kwargs)
        self.pg_ctl = Command(pg_ctl_executable).bake(
            '-w',
            l=self._server_logfile,
            D=self.command.datadir,
            **common_command_kwargs)
        self.psql = Command(psql_executable).bake(**common_command_kwargs)
        self.createdb = Command(createdb_executable).bake(**common_command_kwargs)

    def _create_user(self):
        self.psql('postgres', c="CREATE ROLE {USER} WITH PASSWORD '{PASSWORD}' SUPERUSER LOGIN;".format(**DBSETTINGS))

    def _create_database(self):
        self.createdb('{NAME} OWNER {USER}'.format(**DBSETTINGS))

    def init(self):
        if os.path.exists(self.command.datadir):
            self.command.stderr.write('The data directory ({}) already exists.'.format(self.command.datadir))
            raise SystemExit()
        else:
            self.command.create_datadir_if_not_exists()
            self.pg_ctl('init', '-D', self.command.datadir)
            self.start_database_server()
            self._create_user()
            self._create_database()

            self.command.stdout.write('')
            self.command.stdout.write('='*70)
            self.command.stdout.write('')
            self.command.stdout.write('Successfully:')
            self.command.stdout.write('- Initialized postgres in "{}".'.format(self.command.datadir))
            self.command.stdout.write('- Created the "{USER}"-role with password'.format(**DBSETTINGS))
            self.command.stdout.write('  "{PASSWORD}" and superuser previleges'.format(**DBSETTINGS))
            self.command.stdout.write('- Created an empty database named "{NAME}".'.format(**DBSETTINGS))
            self.command.stdout.write('')
            self.command.stdout.write('The postgres server is running on port {PORT}.'.format(**DBSETTINGS))
            self.command.stdout.write('You can stop it with:')
            self.command.stdout.write('')
            self.command.stdout.write('  $ python manage.py dbdev_stopserver')
            self.command.stdout.write('')
            self.command.stdout.write('='*70)

    def destroy(self):
        self.stop_database_server()
        if os.path.exists(self.command.datadir):
            self.command.remove_datadir()
            self.command.stdout.write('Successfully stopped the Postgres server and removed "{}".'.format(
                self.command.datadir))



    # def _server_is_running(self):
        # return os.path.exists(os.path.join(self.command.datadir, 'postmaster.pid'))

    @property
    def _server_logfile(self):
        return os.path.join(self.command.datadir, 'serverlog.log')

    def run_database_server_in_foreground(self):
        p = self.postgres('-D', self.command.datadir, _bg=True)
        try:
            p.wait()
        except KeyboardInterrupt:
            try:
                self._stop_database_server()
            except ErrorReturnCode:
                p.kill()


    def start_database_server(self):
        self.pg_ctl('start')

    def _stop_database_server(self):
        return self.pg_ctl('stop')

    def stop_database_server(self):
        try:
            self._stop_database_server()
        except ErrorReturnCode:
            pass # The error message from postgres is shown to the user, so no more is needed from us