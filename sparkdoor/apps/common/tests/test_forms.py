"""
test_forms.py - test cases for the `common` app's forms module.
"""
from django.test import TestCase, override_settings

from sparkdoor.libs.httmock import HTTMock
from sparkdoor.libs.factories import UserFactory
from sparkdoor.apps.spark.tests.mocks import spark_cloud_mock
from sparkdoor.apps.spark.tests.factories import DeviceFactory

from .. import forms


spark_test_settings = {
    'CLOUD_USERNAME': 'a_user',
    'CLOUD_PASSWORD': 'password',
    'CLOUD_API_URI': 'https://api.test.com',
}


@override_settings(SPARK=spark_test_settings)
class RegisterDeviceFormTestCase(TestCase):
    """
    Test case for `forms.RegisterDeviceForm`.
    """
    form_class = forms.RegisterDeviceForm

    @classmethod
    def setUpClass(cls):
        """
        Add a test user and device.
        """
        cls.user = UserFactory.create()
        cls.device = DeviceFactory.create(user=cls.user, name='taken', device_id='123')

    def test_taken_device_id(self):
        """
        Test that a taken device id (one that is already in a Device
        entry) will add an error.
        """
        data = { 'user': self.user.id, 'device_id': self.device.device_id, 'name': 'new' }
        form = self.form_class(data)
        self.assertFalse(form.is_valid())
        errors = form.errors.as_data()
        print(errors)
        self.assertEqual(len(errors), 1)
        self.assertIn('device_id', errors.keys())
