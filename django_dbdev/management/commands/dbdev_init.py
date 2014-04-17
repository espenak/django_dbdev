from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings

from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Creates the database configured in the specified --database config.'

    def handle(self, *args, **options):
        self.init(options)
        if self.is_mysql:
            self._create_mysqldb()
        else:
            self.unsupported_database_engine_exit()

    def _create_mysqldb(self):
        self.execute_sql("""

        """)