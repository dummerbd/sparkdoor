"""
base.py - common settings module.
"""
import os


BASE_DIR = os.path.join(os.path.dirname(__file__), '..','..')

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # our apps:
    'sparkdoor.apps.common',
    'groundwork',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.twitter',
    #'allauth.socialaccount.providers.facebook',
)

SECRET_KEY = os.environ['SPARK_SECRET_KEY']

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',


    # Required by allauth template tags
    "django.core.context_processors.request",

    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sparkdoor.urls'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = 'staticfiles'

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'sparkdoor/static'),
)

# Redirect login to home page
LOGIN_REDIRECT_URL = '/'

ADMIN_LOGIN_REDIRECT_URL = '/admin'

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s [%(process)d] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'fallback': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['fallback'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db': {
            'handlers': ['fallback'],
            'level': 'INFO',
            'propogate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propogate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propogate': False,
        },
        'bip': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propogate': False,
        },
    }
}

# Celery settings
BROKER_URL = os.environ['SPARK_CELERY_BROKER_URL']

CELERY_ACCEPT_CONTENT = ['pickle']
