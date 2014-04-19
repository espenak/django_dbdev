from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Drop/delete the database configured in the specified --database config.'

    def dbdev_handle(self):
        self.dbdev_backend.drop_database(self.dbname)