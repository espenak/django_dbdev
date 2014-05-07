from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Destroy the database and all the database server files created by dbdev_init.'

    def dbdev_handle(self):
        self.dbdev_backend.destroy()
