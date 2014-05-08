from shutil import rmtree

from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Remove all the backups for this database backend.'

    def dbdev_handle(self):
        rmtree(self.dbdev_backend.root_backupdir)