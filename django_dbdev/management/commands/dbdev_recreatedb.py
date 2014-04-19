from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Drop/delete and creates the database configured in the specified --database config. If the database does not exist, we just ignore any errors caused by trying to delete it.'

    def dbdev_handle(self):
        try:
            self.dbdev_backend.drop_database(self.dbname)
        except:
            pass
        self.dbdev_backend.create_database(self.dbname)