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
    'CLOUD_API_URI': 'https://api.test.com',
    'CLOUD_RENEW_TOKEN_WINDOW': 60*60 # 1 hour
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
        Add some test dates.
        """
        now = timezone.now()
        cls.expired_dt = now + timedelta(days=-10)
        cls.current_dt = now + timedelta(days=90)
        cls.old_dt = now + timedelta(days=10)

    def test_expires_soon(self):
        """
        Test that `expires_soon` uses the `CLOUD_RENEW_TOKEN_WINDOW` 
        setting.
        """
        now = timezone.now()
        window = spark_test_settings['CLOUD_RENEW_TOKEN_WINDOW']
        cur = self.factory.build(access_token='good',
            expires_at=now + timedelta(seconds=window*2))
        exp = self.factory.build(access_token='expired',
            expires_at=now + timedelta(seconds=window/2))
        self.assertFalse(cur.expires_soon())
        self.assertTrue(exp.expires_soon())

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

    def test_renew_token(self):
        """
        Test that `renew_token` makes a new record and returns the new
        token.
        """
        self.assertEqual(CloudCredentials.objects.count(), 0)
        with HTTMock(spark_cloud_mock):
            token = CloudCredentials.objects.renew_token()
        self.assertEqual(token, ACCESS_TOKEN)
        self.assertEqual(CloudCredentials.objects.count(), 1)
        self.assertEqual(CloudCredentials.objects.first().access_token, token)
        CloudCredentials.objects.all().delete()

    def test_renew_token_not_needed(self):
        """
        Test that `renew_token` only renews the token if needed.
        """
        token = 'good_token'
        cur = self.factory.create(access_token=token, expires_at=self.current_dt)
        with HTTMock(spark_cloud_mock):
            renewed_token = CloudCredentials.objects.renew_token()
        self.assertEqual(renewed_token, token)
        self.assertEqual(CloudCredentials.objects.count(), 1)
        self.assertEqual(CloudCredentials.objects.first().access_token, token)
        CloudCredentials.objects.all().delete()

    def test_discover_tokens(self):
        """
        Test that `discover_tokens` finds new tokens, saves the most
        recent, and returns the token.
        """
        self.assertEqual(CloudCredentials.objects.count(), 0)
        with HTTMock(spark_cloud_mock):
            token = CloudCredentials.objects.discover_tokens()
        self.assertEqual(token, ACCESS_TOKEN)
        self.assertEqual(CloudCredentials.objects.count(), 1)
        self.assertEqual(CloudCredentials.objects.first().access_token, token)

    def test_discover_tokens_exiting_token(self):
        """
        Test that `discover_tokens` does not create a new record if the
        token it finds is already recorded.
        """
        self.factory.create(access_token=ACCESS_TOKEN, expires_at=self.current_dt)
        self.assertEqual(CloudCredentials.objects.count(), 1)
        with HTTMock(spark_cloud_mock):
            token = CloudCredentials.objects.discover_tokens()
        self.assertEqual(token, ACCESS_TOKEN)
        self.assertEqual(CloudCredentials.objects.count(), 1)
        self.assertEqual(CloudCredentials.objects.first().access_token, token)


@override_settings(SPARK=spark_test_settings)
class DeviceTestCase(TestCase):
    """
    Test case for `models.Device`.
    """
    pass
