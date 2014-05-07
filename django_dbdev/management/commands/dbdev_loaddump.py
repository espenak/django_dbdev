from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Load a database dump.'
    args = '<dumpfile>'

    def dbdev_handle(self):
        if len(self.args) != 1:
            self.stderr.write('Dumpfile is required. See --help.')
            raise SystemExit()
        dumpfile = self.args[0]
        self.dbdev_backend.load_dbdump(dumpfile)
