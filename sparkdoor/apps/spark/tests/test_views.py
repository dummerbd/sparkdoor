"""
test_views.py - test cases for the `spark` app's view module.
"""
from django.test import TestCase

from sparkdoor.libs.httmock import HTTMock
from sparkdoor.libs.testmixins import ViewsTestMixin
from sparkdoor.libs.factories import UserFactory

from .factories import DeviceFactory, CloudCredentialsFactory
from .mocks import spark_cloud_mock, ACCESS_TOKEN
from .. import views, models


class DevicesTestView(views.UserDevicesViewBase):
    template_name = 'some_template'


class UserDevicesViewBaseTestCase(ViewsTestMixin, TestCase):
    """
    Test case for `views.UserDevicesViewBase`.
    """
    view_class = DevicesTestView

    @classmethod
    def setUpClass(cls):
        """
        Add test devices.
        """
        cls.user = UserFactory.create()
        cls.devices = [DeviceFactory.create(user=cls.user) for _ in range(3)]
        cls.cred = CloudCredentialsFactory.create(access_token=ACCESS_TOKEN)

    @classmethod
    def tearDownClass(cls):
        """
        CLean up data.
        """
        [d.delete() for d in cls.devices]
        cls.cred.delete()

    def test_context_data(self):
        """
        Test that the `context` includes a `devices` entry.
        """
        response = self.send_request_to_view()
        context = response.context_data
        expected_devices = models.Device.objects.for_user(self.user).order_by('name')
        for i, device in enumerate(expected_devices):
            self.assertEqual(device.id, context['devices'][i].id)

    def test_post(self):
        """
        Test that `post` adds the user to the form.
        """
        data = {'device_id': '123', 'name': 'a name'}
        with HTTMock(spark_cloud_mock):
            resp = self.send_request_to_view(method='POST', user=self.user, data=data)
            post = resp._request.POST
        self.assertIn('user', post)
        self.assertEqual(post['user'], self.user.id)
