import dj_database_url
from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'django-hasker.herokuapp.com'
]
ROOT_URLCONF = 'hasker.urls.production'

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'bormog@gmail.com'
