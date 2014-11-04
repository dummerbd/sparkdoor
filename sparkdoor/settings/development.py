"""
development.py - development-specific settings module.
"""
import os

from .base import *


DEBUG = True

TEMPLATE_DEBUG = True

_db_user = get_env_or_error('SPARK_DATABASE_USER', 'should be the database username')
_db_pass = get_env_or_error('SPARK_DATABASE_PASSWORD', 'should be the database password')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sparkdoor',
        'USER': _db_user,
        'PASSWORD': _db_pass,
        'HOST': 'localhost',
        'PORT': '',
    }
}

# add development-specific apps
INSTALLED_APPS += ('debug_toolbar',)

# add development-specific middleware
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

# used by debug_toolbar
INTERNAL_IPS = ('127.0.0.1',)

# we need to use an explicit setup
DEBUG_TOOLBAR_PATCH_SETTINGS = False

SITE_ID = 2

# show all messages
MESSAGE_LEVEL = 10

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WSGI_APPLICATION = 'sparkdoor.wsgi.development.application'
