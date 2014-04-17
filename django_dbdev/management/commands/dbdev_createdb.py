from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings

from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Creates the database configured in the specified --database config.'

    def dbdev_handle(self):
        self.dbdev_backend.create_database(self.dbname)