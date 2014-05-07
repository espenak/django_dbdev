from django_dbdev.backends.mysql import DBSETTINGS

from .base import *


DATABASES = {
    'default': DBSETTINGS
}