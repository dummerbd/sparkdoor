"""
test_models.py - test cases for the `common` app's models module.
"""
from datetime import datetime, timedelta

from django.test import TestCase

from sparkdoor.apps.spark.tests.factories import DeviceFactory
from .factories import DoorPassFactory
from .. import models


class DoorPassTestCase(TestCase):
    """
    Test case for `models.DoorPass`.
    """
    @classmethod
    def setUpClass(cls):
        """
        Add a test device.
        """
        cls.device = DeviceFactory.create()

    def test_generate_token(self):
        """
        Test that `generate_token` produces a 40-char token string.
        """
        door_pass = DoorPassFactory.build()
        token = door_pass.generate_token()
        self.assertIsInstance(token, str)
        self.assertEqual(len(token), 40)

    def test_save(self):
        """
        Test that `save` adds a value for `token`.
        """
        door_pass = DoorPassFactory.build(token=None, device=self.device)
        door_pass.save()
        self.assertIsNotNone(door_pass.token)

    def test_is_expired_time_based(self):
        """
        Test that `is_expired` works correctly when only using time
        based expiration.
        """
        expired_dt = datetime.now() + timedelta(hours=-1)
        good_dt = datetime.now() + timedelta(hours=1)
        expired_pass = DoorPassFactory.create(device=self.device, expires_at=expired_dt)
        good_pass = DoorPassFactory.create(device=self.device, expires_at=good_dt)
        self.assertTrue(expired_pass.is_expired())
        self.assertFalse(good_pass.is_expired())

    def test_is_exipred_use_base(self):
        """
        Test that `is_expired` works correctly when only using use based
        expiration.
        """
        expired_pass = DoorPassFactory.create(device=self.device, use_limit=2, uses=2)
        good_pass = DoorPassFactory.create(device=self.device, use_limit=2, uses=0)
        self.assertTrue(expired_pass.is_expired())
        self.assertFalse(good_pass.is_expired())
