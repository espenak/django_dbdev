import os.path

from builtins import str
from sh import Command
from sh import ErrorReturnCode
from django.conf import settings

from .base import BaseDbdevBackend

DBSETTINGS = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'PORT': 20021,
    'NAME': 'dbdev',
    'USER': 'dbdev',
    'PASSWORD': 'dbdev',
    'HOST': '127.0.0.1',
}


class PostgresBackend(BaseDbdevBackend):
    def __init__(self, command):
        super(PostgresBackend, self).__init__(command)
        postgres_executable = getattr(settings, 'DBDEV_POSTGRES_EXECUTABLE', 'postgres')
        pg_ctl_executable = getattr(settings, 'DBDEV_POSTGRES_PG_CTL_EXECUTABLE', 'pg_ctl')
        psql_executable = getattr(settings, 'DBDEV_POSTGRES_PSQL_EXECUTABLE', 'psql')
        createdb_executable = getattr(settings, 'DBDEV_POSTGRES_CREATEDB_EXECUTABLE', 'createdb')
        createdb_locale = getattr(settings, 'DBDEV_POSTGRES_CREATEDB_LOCALE', 'en_US.UTF-8')
        pg_dump_executable = getattr(settings, 'DBDEV_POSTGRES_PG_DUMP_EXECUTABLE', 'pg_dump')
        pg_restore_executable = getattr(settings, 'DBDEV_POSTGRES_PG_RESTORE_EXECUTABLE', 'pg_restore')
        self.serverlogfile = os.path.join(self.datadir, 'serverlog.log')
        environ = {
            'PGPORT': str(self.dbsettings['PORT'])
        }
        common_command_kwargs = dict(
            _out=self.sh_stdout_handler,
            _err=self.sh_stderr_handler,
            _env=environ,
            _out_bufsize=1)
        self.postgres = Command(postgres_executable).bake(
            p=self.dbsettings['PORT'],
            **common_command_kwargs)
        self.pg_ctl = Command(pg_ctl_executable).bake(
            '-w',
            l=self._server_logfile,
            D=self.datadir,
            **common_command_kwargs)
        self.psql = Command(psql_executable).bake(
            p=self.dbsettings['PORT'],
            **common_command_kwargs)
        self.createdb = Command(createdb_executable).bake(
            '-e',
            encoding='utf-8',
            template='template0',
            locale=createdb_locale,
            p=self.dbsettings['PORT'],
            **common_command_kwargs)
        self.pg_dump = Command(pg_dump_executable).bake(
            p=self.dbsettings['PORT'],
            dbname=self.dbsettings['NAME'],
            no_privileges=True,
            **common_command_kwargs)
        self.pg_restore = Command(pg_restore_executable).bake(
            p=self.dbsettings['PORT'],
            dbname=self.dbsettings['NAME'],
            no_privileges=True,
            no_acl=True,
            no_owner=True,
            **common_command_kwargs)

    def _create_user(self):
        self.psql('postgres', '-e',
                  c="CREATE ROLE {USER} WITH PASSWORD '{PASSWORD}' SUPERUSER LOGIN;".format(**DBSETTINGS))

    def _create_database(self):
        self.createdb(self.dbsettings['NAME'], owner=self.dbsettings['USER'])

    def init(self):
        if os.path.exists(self.datadir):
            self.stderr.write('The data directory ({}) already exists.'.format(self.datadir))
            raise SystemExit()
        else:
            self.create_datadir_if_not_exists()
            self.pg_ctl('init', '-D', self.datadir)
            self.start_database_server()
            self._create_user()
            self._create_database()

            self.stdout.write('')
            self.stdout.write('=' * 70)
            self.stdout.write('')
            self.stdout.write('Successfully:')
            self.stdout.write('- Initialized postgres in "{}".'.format(self.datadir))
            self.stdout.write('- Created the "{USER}"-role with password'.format(**DBSETTINGS))
            self.stdout.write('  "{PASSWORD}" and superuser previleges'.format(**DBSETTINGS))
            self.stdout.write('- Created an empty database named "{NAME}".'.format(**DBSETTINGS))
            self.stdout.write('')
            self.stdout.write('The postgres server is running on port {PORT}.'.format(**DBSETTINGS))
            self.stdout.write('You can stop it with:')
            self.stdout.write('')
            self.stdout.write('  $ python manage.py dbdev_stopserver')
            self.stdout.write('')
            self.stdout.write('And you can shutdown and destroy the entire setup using:')
            self.stdout.write('')
            self.stdout.write('  $ python manage.py dbdev_destroy')
            self.stdout.write('')
            self.stdout.write('=' * 70)

    def destroy(self):
        self.stop_database_server()
        if os.path.exists(self.datadir):
            self.remove_datadir()
            self.stdout.write('Successfully stopped the Postgres server and removed "{}".'.format(
                self.datadir))

            # def _server_is_running(self):
            # return os.path.exists(os.path.join(self.datadir, 'postmaster.pid'))

    @property
    def _server_logfile(self):
        return os.path.join(self.datadir, 'serverlog.log')

    def run_database_server_in_foreground(self):
        p = self.postgres('-D', self.datadir, _bg=True)
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
            pass  # The error message from postgres is shown to the user, so no more is needed from us

    def load_dbdump(self, dumpfile):
        if dumpfile.endswith('.dump'):
            print(self.pg_restore(dumpfile))
        else:
            self.psql(self.dbsettings['NAME'], f=dumpfile)

    def create_dbdump(self, dumpfile):
        #args = ['-f', dumpfile, '-a', '--column-inserts']
        #for tablename in exclude:
            #args.append('--exclude-table-data={}'.format(tablename))
            #args.append('--exclude-table={}'.format(tablename))
            #args.append('--exclude-schema={}'.format(tablename))
        self.pg_dump(f=dumpfile)

    def backup(self, directory):
        backupfile = os.path.join(directory, 'backup.sql')
        self.pg_dump(f=backupfile)

    def restore(self, directory):
        backupfile = os.path.join(directory, 'backup.sql')
        self.load_dbdump(backupfile)

    def serverinfo(self):
        try:
            self.pg_ctl.status()
        except ErrorReturnCode:
            pass
