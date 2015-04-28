from django_dbdev.backends.postgres import DBSETTINGS

from .base import *


DATABASES = {
    'default': DBSETTINGS
}
# DATABASES['default']['PORT'] = 28001
