from optparse import make_option
# from django.db import connections
from django.core.management.base import BaseCommand
from django.conf import settings

from django_dbdev.dbdev_backendregistry import backendregistry


class BaseDbdevCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--database', dest='database',
                            default='default',
                            help='Nominates a database to work with. Defaults to "default" database.')
        self.add_extra_arguments(parser)

    def add_extra_arguments(self, parser):
        """
        Subclasses can add extra arguments here.
        """

    def handle(self, *args, **options):
        self.args = args
        self.options = options
        self.dbdev_handle()

    @property
    def _dbsettings(self):
        return settings.DATABASES[self.options['database']]

    @property
    def _dbengine(self):
        return self._dbsettings['ENGINE']

    def unsupported_database_engine_exit(self):
        self.stderr.write('Unsupported django_dbdev database engine: {}'.format(self._dbengine))
        self.stderr.write('Supported engines:')
        for engine, backendclass in backendregistry.backends.items():
            self.stderr.write('- {} ({}.{})'.format(engine,
                backendclass.__module__, backendclass.__name__))
        raise SystemExit()

    # def execute_sql(self, sql, params=[]):
    #     cursor = connections[self.options['database']].cursor()
    #     try:
    #         cursor.execute(sql, params)
    #     finally:
    #         cursor.close()

    @property
    def dbdev_backend(self):
        try:
            return backendregistry.backends[self._dbengine](self)
        except KeyError:
            self.unsupported_database_engine_exit()
