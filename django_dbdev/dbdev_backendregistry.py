from django_dbdev.backends.mysql import MySqlBackend
from django_dbdev.backends.postgres import PostgresBackend



class DbdevBackendRegistry(object):
    def __init__(self):
        self.backends = {}

    def register(self, dbengine, backendclass):
        self.backends[dbengine] = backendclass


backendregistry = DbdevBackendRegistry()

def register(dbengine, backendclass):
    """
    Register a dbdev backend to be used for the given Django database engine.
    """
    backendregistry.register(dbengine, backendclass)


backendregistry.register('django.db.backends.mysql', MySqlBackend)
backendregistry.register('django.db.backends.postgresql_psycopg2', PostgresBackend)