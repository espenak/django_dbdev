from optparse import make_option
from django.db import connections
from django.core.management.base import BaseCommand
from django.conf import settings

from django_dbdev.backends.mysql import MySqlBackend


class BaseDbdevCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--database',
            dest='database',
            default='default',
            help='Nominates a database to work with. Defaults to "default" database.'),
        )

    backends = {
        'django.db.backends.mysql': MySqlBackend
    }

    def handle(self, *args, **options):
        self.args = args
        self.options = options
        self.dbdev_handle()


    @property
    def dbsettings(self):
        return settings.DATABASES[self.options['database']]

    @property
    def dbengine(self):
        return self.dbsettings['ENGINE']

    @property
    def dbuser(self):
        return self.dbsettings['USER']

    @property
    def dbpassword(self):
        return self.dbsettings['PASSWORD']

    @property
    def dbname(self):
        return self.dbsettings.get('NAME', None)

    # @property
    # def dbport(self):
    #     return self.dbsettings.get('PORT', None)

    # @property
    # def dbhost(self):
    #     return self.dbsettings.get('HOST', None)

    # @property
    # def is_mysql(self):
    #     return self.dbengine == 'django.db.backends.mysql'

    # @property
    # def is_postgresql(self):
    #     return self.dbengine == 'django.db.backends.postgresql_psycopg2'

    def unsupported_database_engine_exit(self):
        self.stderr.write('Unsupported database engine: {}'.format(self.dbengine))

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