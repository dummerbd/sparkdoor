"""
test_settings.py - test case for the `spark` app's settings module.
"""
from django.test import SimpleTestCase, override_settings
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from ..settings import SparkSettings


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

    def test_username_password_set(self):
        """
        Test that `USERNAME` and `PASSWORD` on `SparkSettings` is
        properly set.
        """
        username, password = 'user', 'pass'
        with self.settings(SPARK={
                'CLOUD_USERNAME': username, 'CLOUD_PASSWORD': password }):
            spark_settings = SparkSettings()
            self.assertEqual(spark_settings.USERNAME, username)
            self.assertEqual(spark_settings.PASSWORD, password)
