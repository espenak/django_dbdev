from django.core.management import call_command

from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Load an SQL database dump.'
    args = '<dumpfile.sql>'

    def add_extra_arguments(self, parser):
        """
        Subclasses can add extra arguments here.
        """
        parser.add_argument('--no-reinit',
                            dest='reinit', action='store_false', default=True,
                            help='Do not run dbdev_reinit before loading the dump.')

    def dbdev_handle(self):
        if len(self.args) != 1:
            self.stderr.write('Dumpfile is required. See --help.')
            raise SystemExit()
        dumpfile = self.args[0]
        if self.options['reinit']:
            call_command('dbdev_reinit', database=self.options['database'])
        self.dbdev_backend.load_sql_dbdump(dumpfile)
