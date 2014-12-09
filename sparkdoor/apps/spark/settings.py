"""
settings.py - module for loading settings for the `spark` app.
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from sparkdoor.libs.utils import str_import

from .apps import DefaultDeviceApp


DEFAULTS = {
    'DEFAULT_APP': DefaultDeviceApp,
    'CLOUD_API_URI': 'https://api.spark.io',
    'CLOUD_RENEW_TOKEN_WINDOW': 60*60*24 # 24 hours
}


def load_apps(apps):
    """
    Load the `APPS` entries. If an entry is a string, than attempt
    to dynamically load it.
    """
    for name, app in apps.items():
        if isinstance(app, str):
            apps[name] = str_import(app)
    return apps


class SparkSettings:
    """
    Class for getting settings from Django's setting. If appropriate
    defaults exist, they should be used, otherwise an exception is
    raised.
    """
    def __init__(self):
        """
        Load spark settings from Django's settings.
        """
        if not hasattr(settings, 'SPARK'):
            raise ImproperlyConfigured('The Spark app requires a configuration object called SPARK in your settings.')

        self.API_URI = settings.SPARK.get('CLOUD_API_URI', DEFAULTS['CLOUD_API_URI'])
        
        self.RENEW_TOKEN_WINDOW = settings.SPARK.get('CLOUD_RENEW_TOKEN_WINDOW',
            DEFAULTS['CLOUD_RENEW_TOKEN_WINDOW'])

        self.USERNAME = settings.SPARK.get('CLOUD_USERNAME', None)
        if self.USERNAME is None:
            raise ImproperlyConfigured('The Spark app requires a CLOUD_USERNAME to be set in the SPARK settings. This should be your login username for your spark cloud service.')

        self.PASSWORD = settings.SPARK.get('CLOUD_PASSWORD', None)
        if self.PASSWORD is None:
            raise ImproperlyConfigured('The Spark app requires a CLOUD_PASSWORD to be set in the SPARK settings. This should be the password for CLOUD_USERNAME.')

        raw_apps = settings.SPARK.get('APPS', None)
        if raw_apps is None:
            raise ImproperlyConfigured('The Spark app requires an APPS dictionary mapping of an app name to a spark.views.DeviceAppBase subclass.')
        self.APPS = load_apps(raw_apps)

        self.DEFAULT_APP = settings.SPARK.get('DEFAULT_APP', DEFAULTS['DEFAULT_APP'])
