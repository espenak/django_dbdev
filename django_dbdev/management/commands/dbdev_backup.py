from optparse import make_option

from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Backup the database.'
    
    option_list = BaseDbdevCommand.option_list + (
        make_option('-n', '--name',
            dest='backupname',
            default=None,
            help='Name the backup. Can be restored with "dbdev_restore -n <name>"'),
        )

    def dbdev_handle(self):
        backupname = self.options['backupname']
        if backupname:
            if self.dbdev_backend.find_named_backupdir(backupname):
                self.stderr.write('A backup named "{} already exists.'.format(backupname))
                raise SystemExit()
        backupdir = self.dbdev_backend.create_timestamped_backupdir(backupname)
        self.dbdev_backend.backup(backupdir)
        self.stdout.write('Successfully created backup in "{}"'.format(backupdir))