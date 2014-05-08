import os.path

from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'List backups in ascending order.'

    def dbdev_handle(self):
        self.stdout.write('Backups sorted with oldest first:')
        for backupdir in sorted(self.dbdev_backend.get_backupdirs()):
            path = os.path.join(self.dbdev_backend.root_backupdir, backupdir)
            self.stdout.write('- {}'.format(path))
