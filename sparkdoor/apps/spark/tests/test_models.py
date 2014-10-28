"""
test_models.py - test cases for the `spark` app's models module.
"""
from datetime import timedelta

from django.test import TestCase, override_settings
from django.utils import timezone

from sparkdoor.libs.httmock import HTTMock

from .mocks import spark_cloud_mock, ACCESS_TOKEN
from .factories import CloudCredentialsFactory, DeviceFactory
from ..models import CloudCredentials, Device
from ..services import SparkCloud


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
        cls.cloud = SparkCloud(spark_test_settings['CLOUD_API_URI'])

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

    def test_refresh_token(self):
        """
        Test that `refresh_token` gets a new token.
        """
        self.assertEqual(CloudCredentials.objects.count(), 0)
        with HTTMock(spark_cloud_mock):
            CloudCredentials.objects.refresh_token()
        self.assertEqual(CloudCredentials.objects.count(), 1)
        self.assertEqual(CloudCredentials.objects.access_token(), ACCESS_TOKEN)
        CloudCredentials.objects.all().delete()

    def test_renew_token(self):
        """
        Test that `_renew_token` makes a new record.
        """
        self.assertEqual(CloudCredentials.objects.count(), 0)
        with HTTMock(spark_cloud_mock):
            CloudCredentials.objects._renew_token(self.cloud)
        self.assertEqual(CloudCredentials.objects.count(), 1)
        self.assertEqual(CloudCredentials.objects.access_token(), ACCESS_TOKEN)
        CloudCredentials.objects.all().delete()

    def test_discover_tokens(self):
        """
        Test that `_discover_tokens` finds new tokens and saves the most
        recent.
        """
        self.assertEqual(CloudCredentials.objects.count(), 0)
        with HTTMock(spark_cloud_mock):
            found = CloudCredentials.objects._discover_tokens(self.cloud)
        self.assertEqual(CloudCredentials.objects.count(), 1)
        self.assertEqual(CloudCredentials.objects.access_token(), ACCESS_TOKEN)

    def test_discover_tokens_existing_token(self):
        """
        Test that `_discover_tokens` does not create a new record if the
        token it finds is already recorded.
        """
        self.factory.create(access_token=ACCESS_TOKEN, expires_at=self.current_dt)
        self.assertEqual(CloudCredentials.objects.count(), 1)
        with HTTMock(spark_cloud_mock):
            found = CloudCredentials.objects._discover_tokens(self.cloud)
        self.assertEqual(CloudCredentials.objects.count(), 1)
        self.assertEqual(CloudCredentials.objects.access_token(), ACCESS_TOKEN)


@override_settings(SPARK=spark_test_settings)
class DeviceTestCase(TestCase):
    """
    Test case for `models.Device`.
    """
    @classmethod
    def setUpClass(cls):
        """
        Add a test device and credentials.
        """
        cls.cred = CloudCredentialsFactory.create(access_token=ACCESS_TOKEN,
            expires_at=timezone.now() + timedelta(days=90))
        cls.cloud = SparkCloud(spark_test_settings['CLOUD_API_URI'], ACCESS_TOKEN)
        with HTTMock(spark_cloud_mock):
            cls.cloud_device = cls.cloud.devices[0]
        cls.device = DeviceFactory.create(device_id=cls.cloud_device.id)

    @classmethod
    def tearDownClass(cls):
        """
        Cleanup test data.
        """
        cls.cred.delete()
        cls.device.delete()

    def test_variables(self):
        """
        Test that `variables` returns the variables available from a
        device.
        """
        with HTTMock(spark_cloud_mock):
            self.assertEqual(self.device.variables, self.cloud_device.variables)

    def test_functions(self):
        """
        Test that `functions` returns the functions available from a
        device.
        """
        with HTTMock(spark_cloud_mock):
            self.assertEqual(self.device.functions, self.cloud_device.functions)
