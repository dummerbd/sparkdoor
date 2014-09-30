import os

from .base import *

DEBUG = True

TEMPLATE_DEBUG = True

_db_user = os.environ['SPARK_DATABASE_USER']
_db_pass = os.environ['SPARK_DATABASE_PASSWORD']

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

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

# show all messages
MESSAGE_LEVEL = 10

# this ID corres
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WSGI_APPLICATION = 'sparkdoor.dev_wsgi.application'
