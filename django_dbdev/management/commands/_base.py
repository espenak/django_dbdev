import os
import os.path
from shutil import rmtree
from optparse import make_option
from django.db import connections
from django.core.management.base import BaseCommand
from django.conf import settings

from django_dbdev.backends.mysql import MySqlBackend
from django_dbdev.backends.postgres import PostgresBackend


class BaseDbdevCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--database',
            dest='database',
            default='default',
            help='Nominates a database to work with. Defaults to "default" database.'),
        )

    backends = {
        'django.db.backends.mysql': MySqlBackend,
        'django.db.backends.postgresql_psycopg2': PostgresBackend,
    }

    def handle(self, *args, **options):
        self.args = args
        self.options = options
        self.dbdev_handle()

    @property
    def root_datadir_path(self):
        return getattr(settings, 'DBDEV_DATADIR', 'dbdev_tempdata')

    def create_datadir_if_not_exists(self):
        if not os.path.exists(self.datadir):
            os.makedirs(self.datadir)

    def remove_datadir(self):
        rmtree(self.datadir)


    @property
    def datadir(self):
        """
        Get the path to the temporary data directory for this database.

        The directory is created if it does not exist.
        """
        path = os.path.join(self.root_datadir_path, self.dbengine)
        return path

    @property
    def dbsettings(self):
        return settings.DATABASES[self.options['database']]

    @property
    def dbengine(self):
        return self.dbsettings['ENGINE']

    def unsupported_database_engine_exit(self):
        self.stderr.write('Unsupported django_dbdev database engine: {}'.format(self.dbengine))
        raise SystemExit()

    def execute_sql(self, sql, params=[]):
        cursor = connections[self.options['database']].cursor()
        try:
            cursor.execute(sql, params)
        finally:
            cursor.close()

    @property
    def dbdev_backend(self):
        try:
            return self.backends[self.dbengine](self)
        except KeyError:
            self.unsupported_database_engine_exit()