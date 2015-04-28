from django_dbdev.backends.postgres import DBSETTINGS

from .base import *


DATABASES = {
    'default': DBSETTINGS
}
# DBDEV_POSTGRES_PORT = 28001
