"""
heroku.py - production-specific settings module for Heroku.
"""
from .base import *

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = { 'default': dj_database_url.config() }

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Don't show DEBUG (10) level messages
MESSAGE_LEVEL = 20

LOGGING['root'] = { 'level': MESSAGE_LEVEL }

STATIC_ROOT = 'staticfiles'

SITE_ID = 2

# Relies on Heroku's sendgrid addon
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = get_env_or_error('SENDGRID_USERNAME', 'check that the Sendgrid addon has been installed.')
EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_PASSWORD", 'check that the Sendgrid addon has been installed.')
EMAIL_PORT = 25
EMAIL_USE_TLS = False

WSGI_APPLICATION = 'sparkdoor.wsgi.heroku.application'
