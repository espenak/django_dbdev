
class BaseDbdevBackend(object):

    def drop_user(self):
        """
        Delete/drop the user created by :meth:`.create_user`.
        """
        raise NotImplementedError()

    def create_user(self, user, password):
        """
        Create the Django database user.
        """
        raise NotImplementedError()

    def create_database(self, dbname):
        """
        Create the database with the given ``dbname``.
        """
        raise NotImplementedError()

    def drop_database(self, dbname):
        """
        Drop/delete the database with the given ``dbname``.
        """
        raise NotImplementedError()