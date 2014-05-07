from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Same as running dbdev_destroy followed by dbdev_init.'

    def dbdev_handle(self):
        self.dbdev_backend.destroy()
        self.dbdev_backend.init()
