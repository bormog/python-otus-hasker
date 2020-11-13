import dj_database_url
from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'django-hasker.herokuapp.com'
]
ROOT_URLCONF = 'hasker.urls.production'

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
