from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Create a database dump.'

    def add_extra_arguments(self, parser):
        parser.add_argument('dumpfile')
        #parser.add_argument(
                #'--exclude', dest='exclude',
                #nargs='*',
                #help='Exclude the given table. Example: "--exclude tableA tableB tableC".')

    def dbdev_handle(self):
        dumpfile = self.options['dumpfile']
        #exclude = self.options['exclude']
        self.dbdev_backend.create_dbdump(dumpfile)
