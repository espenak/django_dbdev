import os.path

from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'List backups in ascending order.'

    def dbdev_handle(self):
        backupdirs = self.dbdev_backend.get_backupdirs()
        if backupdirs:
            self.stdout.write('Backups sorted with oldest first:')
            for backupdir in sorted(backupdirs):
                path = os.path.join(self.dbdev_backend.root_backupdir, backupdir)
                self.stdout.write('- {}'.format(path))
        else:
            self.stderr.write('No backups. Use dbdev_backup to make backups.')