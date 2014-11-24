"""
test_serives.py - unit tests for the `spark` app's services module.
"""
from datetime import datetime

from django.test import SimpleTestCase, override_settings

from sparkdoor.libs.httmock import HTTMock

from .mocks import spark_cloud_mock, ACCESS_TOKEN
from ..services import SparkCloud, CloudDevice, ServiceError


spark_test_settings = {
    'CLOUD_USERNAME': 'a_user',
    'CLOUD_PASSWORD': 'password',
    'CLOUD_API_URI': 'https://api.test.com',
    'APPS': {}
}


@override_settings(SPARK=spark_test_settings)
class SparkCloudTestCase(SimpleTestCase):
    """
    Test case for `services.SparkCloud`.
    """
    @classmethod
    def setUpClass(cls):
        """
        Add test settings shortcuts.
        """
        cls.USERNAME = spark_test_settings['CLOUD_USERNAME']
        cls.PASSWORD = spark_test_settings['CLOUD_PASSWORD']
        cls.API_URI = spark_test_settings['CLOUD_API_URI']

    def test_init(self):
        """
        Test that `__int___` sets the `access_token` and `api_uri`
        attributes.
        """
        token = 'a token'
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud(self.API_URI, token)
        self.assertEqual(cloud.access_token, token)

    def test_renew_token(self):
        """
        Test that `renew_token` requests a new token using the provided
        `username` and `password`.
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud(self.API_URI)
            token, expires = cloud.renew_token(self.USERNAME, self.PASSWORD)
        self.assertEqual(token, cloud.access_token)
        self.assertEqual(token, ACCESS_TOKEN)
        self.assertIsInstance(expires, datetime)

    def test_renew_token_with_invalid_credentials(self):
        """
        Test that `renew_token` returns (None, None) with invalid
        credentials.
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud(self.API_URI)
            token, expires = cloud.renew_token('not_a_valid_user', 'password')
        self.assertIsNone(cloud.access_token)
        self.assertIsNone(token)
        self.assertIsNone(expires)

    def test_discover_tokens(self):
        """
        Test that `discover_tokens` returns the most recent token in a
        tuple (token, expires_by).
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud(self.API_URI)
            token, expires = cloud.discover_tokens(self.USERNAME, self.PASSWORD)
        self.assertEqual(token, cloud.access_token)
        self.assertEqual(token, ACCESS_TOKEN)
        self.assertIsInstance(expires, datetime)

    def test_discover_tokens_with_invalid_credentials(self):
        """
        Test that `discover_tokens` returns (None, None) with invalid
        credentials.
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud(self.API_URI)
            token, expires = cloud.discover_tokens('not_a_valid_user', 'password')
        self.assertIsNone(token)
        self.assertIsNone(expires)

    def test_all_devices(self):
        """
        Test that `all_devices` returns a list of available `CloudDevice` 
        instances.
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud(self.API_URI, ACCESS_TOKEN)
            devices = cloud.all_devices()
        self.assertIsInstance(devices, list)
        self.assertTrue(len(devices) > 0)
        for d in devices:
            self.assertIsInstance(d, CloudDevice)
            self.assertEqual(cloud, d.cloud)

    def test_all_devices_with_invalid_access_token(self):
        """
        Test that `all_devices` returns an empty list when an invalid
        access token is used.
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud(self.API_URI, 'invalid_token')
            devices = cloud.all_devices()
        self.assertEqual(devices, [])

    def test_device_with_invalid_access_token(self):
        """
        Test that `device` returns None when an invalid access token is
        used.
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud(self.API_URI, 'invalid_token')
            device = cloud.device('123')
        self.assertIsNone(device)

    def test_device_with_nonexistant_device_id(self):
        """
        Test that `device` returns None when an invalid access token is
        used.
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud(self.API_URI, ACCESS_TOKEN)
            device = cloud.device('not_a_device_id')
        self.assertIsNone(device)

    def test_device(self):
        """
        Test that `device` returns a new `CloudDevice`.
        """
        with HTTMock(spark_cloud_mock):
            cloud = SparkCloud(self.API_URI, ACCESS_TOKEN)
            device_id = cloud.all_devices()[0].id
            device = cloud.device(device_id)
        self.assertIsInstance(device, CloudDevice)


@override_settings(SPARK=spark_test_settings)
class CloudDeviceTestCase(SimpleTestCase):
    """
    Test case for `services.CloudDevice`.
    """
    @classmethod
    def setUpClass(cls):
        """
        Add test settings shortcuts.
        """
        cls.API_URI = spark_test_settings['CLOUD_API_URI']

    def test_functions(self):
        """
        Test that `functions` contains a list of available function
        names.
        """
        with HTTMock(spark_cloud_mock):
            device = SparkCloud(self.API_URI, ACCESS_TOKEN).all_devices()[0]
            self.assertIsNotNone(device.functions)

    def test_variables(self):
        """
        Test that `variables` contains a dictionary mapping of a name to
        a variable type.
        """
        with HTTMock(spark_cloud_mock):
            device = SparkCloud(self.API_URI, ACCESS_TOKEN).all_devices()[0]
            for var_name, var_type in device.variables.items():
                self.assertIsInstance(var_name, str)
                self.assertIn(var_type, ['int32', 'double', 'string'])

    def test_call_nonexistant_function(self):
        """
        Test that `call` raises `ServiceError` when a nonexistant
        function name is used.
        """
        with HTTMock(spark_cloud_mock):
            device = SparkCloud(self.API_URI, ACCESS_TOKEN).all_devices()[0]
            with self.assertRaises(ServiceError):
                ret = device.call('not_a_function', 'some args')

    def test_call(self):
        """
        Test that `call` returns an int after a successful call.
        """
        with HTTMock(spark_cloud_mock):
            device = SparkCloud(self.API_URI, ACCESS_TOKEN).all_devices()[0]
            func_name = device.functions[0]
            ret = device.call(func_name, 'some args')
        self.assertIsInstance(ret, int)

    def test_read_nonexistant_variable(self):
        """
        Test that `read` raises a `ServiceError` when a nonexistant
        variable name is used.
        """
        with HTTMock(spark_cloud_mock):
            device = SparkCloud(self.API_URI, ACCESS_TOKEN).all_devices()[0]
            with self.assertRaises(ServiceError):
                ret = device.read('not_a_variable')

    def test_read(self):
        """
        Test that `read` returns either an `int`, `float`, or `string`.
        """
        with HTTMock(spark_cloud_mock):
            device = SparkCloud(self.API_URI, ACCESS_TOKEN).all_devices()[0]
            for name in device.variables.keys():
                val = device.read(name)
                self.assertIsInstance(val, (int, float, str))
