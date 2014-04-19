from optparse import make_option

from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Creates the role/user with the permissions required for working with the specified --database.'
    option_list = BaseDbdevCommand.option_list + (
        make_option('-u', '--adminuser',
            dest='adminuser',
            default='root',
            help='A database user with the permission to create users/roles. Defaults to "root".'),
        make_option('-p', '--adminuserpassword',
            dest='adminuserpassword',
            default='secret',
            help='The password of the --adminuser. Defaults to "secret".'),
    )

    def dbdev_handle(self):
        adminuser = self.options['adminuser']
        adminuserpassword = self.options['adminuserpassword']
        self.dbdev_backend.create_user(adminuser=adminuser, adminuserpassword=adminuserpassword)