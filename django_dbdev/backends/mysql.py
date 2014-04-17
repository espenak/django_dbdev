from subprocess import check_call
from django.db.utils import ConnectionHandler
from django.conf import settings


class MySqlBackend(object):
    def __init__(self, command):
        self.command = command

    # @property
    # def _mysqld_executable(self):
    #     return getattr(settings, 'MYSQLD_PATH', 'mysqld')

    def cursor_without_db(self, user=None, password=None):
        """
        Get a DB API cursor that is not connected to a database.
        """
        dbsettings = {}
        dbsettings.update(self.command.dbsettings)
        del dbsettings['NAME'] # When we do not configure a name, the cursor will no connect to a database

        if user:
            dbsettings['USER'] = user
        if password:
            dbsettings['PASSWORD'] = password

        cursor = ConnectionHandler({
            'django_dbdev': dbsettings
        })['django_dbdev'].cursor()
        return cursor

    def drop_user(self, **auth):
        cursor = self.cursor_without_db(**auth)
        try:
            cursor.execute("DROP USER %s@'localhost';", [self.command.dbuser])
        finally:
            cursor.close()

    def create_user(self, **auth):
        cursor = self.cursor_without_db(**auth)
        try:
            cursor.execute("CREATE USER %s@'localhost' IDENTIFIED BY %s;",
                [self.command.dbuser, self.command.dbpassword])
            cursor.execute("GRANT ALL PRIVILEGES ON *.* TO %s@'localhost';",
                [self.command.dbuser])
        finally:
            cursor.close()

    def create_database(self, dbname):
        cursor = self.cursor_without_db()
        try:
            cursor.execute('CREATE DATABASE {};'.format(dbname)) # NOTE: Using params for dbname does not work for some reason!
        finally:
            cursor.close()