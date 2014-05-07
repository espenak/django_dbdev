from sh import Command
from sh import ErrorReturnCode
import os.path
from django.db.utils import ConnectionHandler
from django.conf import settings


class PostgresBackend(object):
    def __init__(self, command):
        self.command = command
        postgres_executable = getattr(settings, 'DBDEV_POSTGRES_EXECUTABLE', 'postgres')
        pg_ctl_executable = getattr(settings, 'DBDEV_PG_CTL_EXECUTABLE', 'pg_ctl')
        self.postgres = Command(postgres_executable).bake(
            _out=self.command.stdout,
            _err=self.command.stderr,
            _out_bufsize=1)
        self.pg_ctl = Command(pg_ctl_executable).bake(
            '-l', self._server_logfile,
            '-D', self.command.datadir,
            _out=self.command.stdout,
            _err=self.command.stderr,
            _out_bufsize=1)


    def _cursor_without_db(self, user=None, password=None):
        """
        Get a DB API cursor that is not connected to a database.
        """
        dbsettings = {}
        dbsettings.update(self.command.dbsettings)
        del dbsettings['NAME'] # When we do not configure a name, the cursor will not connect to a database

        if user:
            dbsettings['USER'] = user
        if password:
            dbsettings['PASSWORD'] = password

        cursor = ConnectionHandler({
            'django_dbdev': dbsettings
        })['django_dbdev'].cursor()
        return cursor

    def drop_user(self):
        cursor = self._cursor_without_db()
        try:
            cursor.execute("DROP USER %s@'localhost';", [self.command.dbuser])
        finally:
            cursor.close()

    def create_user(self, adminuser, adminuserpassword):
        cursor = self._cursor_without_db(adminuser, adminuserpassword)
        try:
            cursor.execute("CREATE USER %s@'localhost' IDENTIFIED BY %s;",
                [self.command.dbuser, self.command.dbpassword])
            cursor.execute("GRANT ALL PRIVILEGES ON *.* TO %s@'localhost';",
                [self.command.dbuser])
        finally:
            cursor.close()

    def create_database(self, dbname):
        cursor = self._cursor_without_db()
        try:
            cursor.execute('CREATE DATABASE {};'.format(dbname)) # NOTE: Using params for dbname does not work for some reason!
        finally:
            cursor.close()

    def drop_database(self, dbname):
        cursor = self._cursor_without_db()
        try:
            cursor.execute('DROP DATABASE {};'.format(dbname)) # NOTE: Using params for dbname does not work for some reason!
        finally:
            cursor.close()

    def _init_datadir_if_needed(self):
        if not os.path.exists(os.path.join(self.command.datadir, 'postgresql.conf')):
            self.create_datadir_if_not_exists()
            self.pg_ctl('init', '-D', self.command.datadir)

    # def _server_is_running(self):
        # return os.path.exists(os.path.join(self.command.datadir, 'postmaster.pid'))

    @property
    def _server_logfile(self):
        return os.path.join(self.command.datadir, 'serverlog.log')

    def run_database_server_in_foreground(self):
        self._init_datadir_if_needed()
        p = self.postgres('-D', self.command.datadir,
            _bg=True)
        try:
            p.wait()
        except KeyboardInterrupt:
            try:
                self._stop_database_server()
            except ErrorReturnCode:
                p.kill()

    def start_database_server(self):
        self._init_datadir_if_needed()
        self.pg_ctl('start')


    def _stop_database_server(self):
        return self.pg_ctl('stop')

    def stop_database_server(self):
        try:
            self._stop_database_server()
        except ErrorReturnCode:
            pass # The error message from postgres is shown to the user, so no more is needed from us