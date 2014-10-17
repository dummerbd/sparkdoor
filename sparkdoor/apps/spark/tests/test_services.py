"""
test_serives.py - unit tests for the `spark` app's services module.
"""
from django.test import SimpleTestCase, override_settings

from sparkdoor.libs.httmock import HTTMock

from .mocks import spark_cloud_mock
from ..services import SparkCloud


spark_test_settings = {
    'CLOUD_USERNAME': 'a_user',
    'CLOUD_PASSWORD': 'password',
    'CLOUD_API_URI': 'https://api.test.com'
}

@override_settings(SPARK=spark_test_settings)
class SparkCloudTestCase(SimpleTestCase):
    """
    Test case for `services.SparkCloud`.
    """
    def test_constructor(self):
        """
        Test that constructing a new `SparkCloud` object populates the
        access token using login credentials in `SparkSettings`.
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud(access_token='')
        self.assertIsNotNone(cloud.access_token)

    def test_login_with_invalid_credentials(self):
        """
        Test that `_login` returns None with invalid credentials.
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud('')
            token = cloud._login('not_a_valid_user', 'password')
        self.assertIsNone(token)
        self.assertIsNone(cloud.access_token)
