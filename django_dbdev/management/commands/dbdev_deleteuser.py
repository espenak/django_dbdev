from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings

from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Drop/delete the role/user created with dbdev_createuser.'
    option_list = BaseDbdevCommand.option_list + (
        make_option('-u', '--adminuser',
            dest='adminuser',
            default='root',
            help='A database user with the permission to drop/delete users. Defaults to "root".'),
        make_option('-p', '--adminuserpassword',
            dest='adminuserpassword',
            default='secret',
            help='The password of the --adminuser. Defaults to "secret".'),
    )

    def dbdev_handle(self):
        adminuser = self.options['adminuser']
        adminuserpassword = self.options['adminuserpassword']
        self.dbdev_backend.drop_user(user=adminuser, password=adminuserpassword)