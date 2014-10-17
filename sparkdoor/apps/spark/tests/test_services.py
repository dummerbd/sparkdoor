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
    def test_login_with_valid_credentials(self):
        """
        Test that `login` returns an access token and sets the
        `access_token` attribute after a successful login.
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud()
            token = cloud.login()
        self.assertIsNotNone(token)
        self.assertEqual(token, cloud.access_token)

    def test_login_with_invalid_credentials(self):
        """
        Test that `login` returns None with invalid credentials.
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud()
            token = cloud.login('not_a_valid_user', 'password')
        self.assertIsNone(token)
        self.assertIsNone(cloud.access_token)
