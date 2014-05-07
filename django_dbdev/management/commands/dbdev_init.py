from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Create and setup the database.'

    def dbdev_handle(self):
        self.dbdev_backend.init()
