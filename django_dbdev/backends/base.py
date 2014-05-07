from django.db.utils import ConnectionHandler



class BaseDbdevBackend(object):
    # def drop_user(self):
    #     """
    #     Delete/drop the user created by :meth:`.create_user`.
    #     """
    #     raise NotImplementedError()

    # def create_user(self, user, password):
    #     """
    #     Create the Django database user.
    #     """
    #     raise NotImplementedError()

    # def create_database(self, dbname):
    #     """
    #     Create the database with the given ``dbname``.
    #     """
    #     raise NotImplementedError()

    # def drop_database(self, dbname):
    #     """
    #     Drop/delete the database with the given ``dbname``.
    #     """
    #     raise NotImplementedError()

    def init(self):
        """
        Create the database and grant the required previleges to
        the database user.
        """
        raise NotImplementedError()

    def destroy(self):
        """
        Remove all the files for the database.

        Typically stops any running database server and deletes
        the data directory.
        """
        raise NotImplementedError()

    def run_database_server_in_foreground(self):
        """
        Run database server in the foreground.
        """
        raise NotImplementedError()

    def start_database_server(self):
        """
        Start database server in the background.
        """
        raise NotImplementedError()

    def stop_database_server(self):
        """
        Stop database server started with :meth:`.start_database_server`.
        """
        raise NotImplementedError()