import os.path
from optparse import make_option

from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Restore backup created with dbdev_backup.'
    args = '[backup-directory]'

    def add_extra_arguments(self, parser):
        """
        Subclasses can add extra arguments here.
        """
        parser.add_argument(
            '-n', '--name',
            dest='backupname',
            default=None,
            help='Name of backup to restore if a backup was created with "dbdev_backup -n <name>".'),

    def dbdev_handle(self):
        if len(self.args) == 0:
            if self.options['backupname']:
                backupdir = self.dbdev_backend.find_named_backupdir(self.options['backupname'])
            else:
                try:
                    backupdir = self.dbdev_backend.get_last_backupdir()
                except IndexError:
                    self.stderr.write('You have no backups for this database.')
                    raise SystemExit()
        else:
            backupdir = self.args[0]
            if not os.path.isdir(backupdir):
                self.stderr.write('The first argument must be a directory!')
                raise SystemExit()

        self.dbdev_backend.reinit()
        self.dbdev_backend.restore(backupdir)
        self.stdout.write('Successfully restored backup from "{}"'.format(backupdir))
