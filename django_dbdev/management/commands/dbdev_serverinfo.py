from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Print server info to stdout. The output is database specific.'

    def dbdev_handle(self):
        self.dbdev_backend.serverinfo()