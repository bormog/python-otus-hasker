from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Disable Auth Password Validators
AUTH_PASSWORD_VALIDATORS = []

# Questions App
QUESTIONS_PER_PAGE = 3
ANSWERS_PER_PAGE = 3

# Email
EMAIL_SUBJECT_PREFIX = '[Hasker]'
DEFAULT_FROM_EMAIL = 'hasker@hasker.com'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'tmp' / 'emails'

