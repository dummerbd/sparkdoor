"""
settings.py - module for loading settings for the `spark` app.
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


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
        self.USERNAME = settings.SPARK.get('CLOUD_USERNAME', None)
        if self.USERNAME is None:
            raise ImproperlyConfigured('The Spark app requires a CLOUD_USERNAME to be set in the SPARK settings. This should be your login username for your spark cloud service.')
        self.PASSWORD = settings.SPARK.get('CLOUD_PASSWORD', None)
        if self.PASSWORD is None:
            raise ImproperlyConfigured('The Spark app requires a CLOUD_PASSWORD to be set in the SPARK settings. This should be the password for CLOUD_USERNAME.')
