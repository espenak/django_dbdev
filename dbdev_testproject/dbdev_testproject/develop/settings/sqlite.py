from django_dbdev.backends.sqlite import DBSETTINGS

from .base import *


DATABASES = {
    'default': DBSETTINGS
}