"""
test_tasks.py - test cases for the `spark` app's tasks module.
"""
from datetime import timedelta

from django.test import TestCase, override_settings
from django.utils import timezone

from sparkdoor.libs.httmock import HTTMock

from .mocks import spark_cloud_mock, ACCESS_TOKEN
from .factories import CloudCredentialsFactory
from ..tasks import refresh_access_token
from ..models import CloudCredentials


spark_test_settings = {
    'CLOUD_USERNAME': 'a_user',
    'CLOUD_PASSWORD': 'password',
    'CLOUD_API_URI': 'https://api.test.com'
}


@override_settings(SPARK=spark_test_settings)
class RefreshAccessTokenTestCase(TestCase):
    """
    Test case for `tasks.refresh_access_token`.
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

    def test_returns_good_token(self):
        """
        If there is a good token (not expired) then don't do anything,
        just return that token.
        """
        self.assertEqual(CloudCredentials.objects.count(), 0)
        cred = self.factory.create(access_token='good_token', expires_at=self.current_dt)
        with HTTMock(spark_cloud_mock):
            token = refresh_access_token()
        self.assertEqual(CloudCredentials.objects.count(), 1)
        self.assertEqual(token, 'good_token')
        cred.delete()

    def test_renews_token(self):
        """
        If there isn't any good tokens then renew one.
        """
        self.assertEqual(CloudCredentials.objects.count(), 0)
        cred = self.factory.create(access_token='old_token', expires_at=self.expired_dt)
        with HTTMock(spark_cloud_mock):
            token = refresh_access_token()
        self.assertEqual(CloudCredentials.objects.count(), 2)
        self.assertEqual(token, ACCESS_TOKEN)
        cred.delete()
