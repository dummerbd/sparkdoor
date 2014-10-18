"""
test_models.py - test cases for the `spark` app's models module.
"""
from datetime import timedelta

from django.test import TestCase, override_settings
from django.utils import timezone

from sparkdoor.libs.httmock import HTTMock

from .mocks import spark_cloud_mock, ACCESS_TOKEN
from .factories import CloudCredentialsFactory
from ..models import CloudCredentials, Device


spark_test_settings = {
    'CLOUD_USERNAME': 'a_user',
    'CLOUD_PASSWORD': 'password',
    'CLOUD_API_URI': 'https://api.test.com'
}


@override_settings(SPARK=spark_test_settings)
class CloudCredentialsTestCase(TestCase):
    """
    Test case for `models.CloudCredentials`.
    """
    factory = CloudCredentialsFactory

    @classmethod
    def setUpClass(cls):
        """
        Add some test data.
        """
        now = timezone.now()
        cls.expired_dt = now + timedelta(days=-10)
        cls.current_dt = now + timedelta(days=90)
        cls.old_dt = now + timedelta(days=10)

    def test_access_token(self):
        """
        Test that `access_token` returns the most recent token that
        is not expired.
        """
        exp = self.factory.create(access_token='expired', expires_at=self.expired_dt)
        cur = self.factory.create(access_token=ACCESS_TOKEN, expires_at=self.current_dt)
        old = self.factory.create(access_token='old', expires_at=self.old_dt)
        with HTTMock(spark_cloud_mock):
            token = CloudCredentials.objects.access_token()
        self.assertEqual(token, ACCESS_TOKEN)
        CloudCredentials.objects.all().delete()

    def test_access_token_empty(self):
        """
        Test that `access_token` returns None if there isn't any saved
        credentials.
        """
        self.assertEqual(CloudCredentials.objects.count(), 0)
        with HTTMock(spark_cloud_mock):
            token = CloudCredentials.objects.access_token()
        self.assertEqual(token, None)

    def test_access_token_all_expired(self):
        """
        Test that `access_token` returns None if all the stored tokens
        are expired.
        """
        exp = self.factory.create(access_token='expired', expires_at=self.expired_dt)
        with HTTMock(spark_cloud_mock):
            token = CloudCredentials.objects.access_token()
        self.assertEqual(token, None)
        exp.delete()


@override_settings(SPARK=spark_test_settings)
class DeviceTestCase(TestCase):
    """
    Test case for `models.Device`.
    """
    pass
