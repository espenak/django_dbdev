from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Run the database server for the database specified in the --database config in the foreground.'

    def dbdev_handle(self):
        self.dbdev_backend.run_database_server_in_foreground()

