from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Drop/delete the role/user created with dbdev_createuser.'

    def dbdev_handle(self):
        self.dbdev_backend.drop_user()