"""
test_settings.py - test case for the `spark` app's settings module.
"""
from django.test import SimpleTestCase, override_settings
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from ..settings import SparkSettings, DEFAULTS


class SparkSettingsTestCase(SimpleTestCase):
    """
    Test case for `settings.SparkSettings`.
    """
    @override_settings()
    def test_spark_must_be_defined(self):
        """
        Test that the `SPARK` config must be defined.
        """
        del settings.SPARK
        with self.assertRaises(ImproperlyConfigured):
            spark_settings = SparkSettings()

    @override_settings(SPARK={ 'CLOUD_USERNAME': '...', 'CLOUD_PASSWORD': '...' })
    def test_cloud_api_uri_has_default(self):
        """
        Test the `SPARK.CLOUD_API_URI` defaults properly when not 
        defined.
        """
        self.assertIsNone(settings.SPARK.get('CLOUD_API_URI', None))
        spark_settings = SparkSettings()
        self.assertEqual(spark_settings.API_URI, DEFAULTS['CLOUD_API_URI'])

    @override_settings(SPARK={ 'CLOUD_PASSWORD': '...' })
    def test_cloud_username_must_be_defined(self):
        """
        Test that `SPARK.CLOUD_USERNAME` must be defined.
        """
        self.assertIsNone(settings.SPARK.get('CLOUD_USERNAME', None))
        with self.assertRaises(ImproperlyConfigured):
            spark_settings = SparkSettings()

    @override_settings(SPARK={ 'CLOUD_USERNAME': '...' })
    def test_cloud_password_must_be_defined(self):
        """
        Test that `SPARK.CLOUD_PASSWORD` must be defined.
        """
        self.assertIsNone(settings.SPARK.get('CLOUD_PASSWORD', None))
        with self.assertRaises(ImproperlyConfigured):
            spark_settings = SparkSettings()

    def test_settings(self):
        """
        Test that settings in `SPARK` are properly assigned into the
        `SparkSettings` instance.
        """
        username, password = 'user', 'pass'
        api_uri = 'http://api.somewhere.com'
        with self.settings(SPARK={
                'CLOUD_USERNAME': username, 'CLOUD_PASSWORD': password,
                'CLOUD_API_URI': api_uri }):
            spark_settings = SparkSettings()
            self.assertEqual(spark_settings.API_URI, api_uri)
            self.assertEqual(spark_settings.USERNAME, username)
            self.assertEqual(spark_settings.PASSWORD, password)
