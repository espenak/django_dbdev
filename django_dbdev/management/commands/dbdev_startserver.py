from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Start the database server for the database specified in the --database config.'

    def dbdev_handle(self):
        self.dbdev_backend.start_database_server()
