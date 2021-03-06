"""
test_forms.py - test cases for the `common` app's forms module.
"""
from django.test import TestCase, override_settings

from sparkdoor.libs.httmock import HTTMock
from sparkdoor.libs.factories import UserFactory

from .mocks import spark_cloud_mock, ACCESS_TOKEN
from .factories import CloudCredentialsFactory, DeviceFactory
from ..services import SparkCloud, ServiceError
from .. import forms


spark_test_settings = {
    'CLOUD_USERNAME': 'a_user',
    'CLOUD_PASSWORD': 'password',
    'CLOUD_API_URI': 'https://api.test.com',
    'APPS': {}
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
        cls.api_uri = spark_test_settings['CLOUD_API_URI']
        cls.user = UserFactory.create()
        cls.device = DeviceFactory.create(user=cls.user, name='taken', device_id='123')
        cls.cred = CloudCredentialsFactory.create(access_token=ACCESS_TOKEN)
        with HTTMock(spark_cloud_mock):
            cls.cloud_device = SparkCloud(cls.api_uri, ACCESS_TOKEN).all_devices()[0]

    @classmethod
    def tearDownClass(cls):
        """
        Clean up test data.
        """
        cls.device.delete()
        cls.cred.delete()

    def test_taken_device_id(self):
        """
        Test that a taken device id (one that is already in a Device
        entry) will add an error.
        """
        data = { 'user': self.user.id, 'device_id': self.device.device_id, 'name': 'new' }
        with HTTMock(spark_cloud_mock):
            form = self.form_class(data)
            errors = form.errors.as_data()
        self.assertEqual(len(errors), 1)
        self.assertIn('device_id', errors.keys())

    def test_nonexistant_device_id(self):
        """
        Test that a device id that isn't on the Spark cloud creates a
        field error.
        """
        data = { 'user': self.user.id, 'device_id': 'not_an_id', 'name': 'new' }
        with HTTMock(spark_cloud_mock):
            form = self.form_class(data)
            self.assertFalse(form.is_valid())
            errors = form.errors.as_data()
        self.assertEqual(len(errors), 1)
        self.assertIn('device_id', errors.keys())

    def test_unreachable_device(self):
        """
        Test that an unconnected device (which will raise a ServiceError)
        adds an error to the `device_id` field.
        """
        data = { 'user': self.user.id, 'device_id': self.cloud_device.id, 'name': 'new' }
        real_device_read = self.cloud_device.read
        def fake_device_read(var):
            raise ServiceError
        self.cloud_device.read = fake_device_read

        with HTTMock(spark_cloud_mock):
            form = self.form_class(data)
            form._get_app_name(self.cloud_device)
            errors = form.errors.as_data()
        self.assertEqual(len(errors), 1)
        self.assertIn('device_id', errors.keys())

        self.cloud_device.read = real_device_read

    def test_good_device_id(self):
        """
        Test that a form with a valid device id is valid.
        """
        data = { 'user': self.user.id, 'device_id': self.cloud_device.id, 'name': 'new' }
        with HTTMock(spark_cloud_mock):
            expected_app_name = self.cloud_device.read('app_name')
            form = self.form_class(data)
            self.assertTrue(form.is_valid())
        self.assertEqual(expected_app_name, form.cleaned_data['app_name'])
