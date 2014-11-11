"""
test_views.py - test cases for the `common` app's view module.
"""
from django.test import SimpleTestCase, TestCase

from sparkdoor.libs.httmock import HTTMock
from sparkdoor.libs.testmixins import ViewsTestMixin
from sparkdoor.libs.factories import UserFactory
from sparkdoor.apps.spark.models import Device
from sparkdoor.apps.spark.tests.factories import DeviceFactory, CloudCredentialsFactory
from sparkdoor.apps.spark.tests.mocks import spark_cloud_mock, ACCESS_TOKEN

from .. import views


class HomeViewTestCase(ViewsTestMixin, SimpleTestCase):
    """
    Test case for `views.HomeView`.
    """
    view_class = views.HomeView

    def test_correct_template(self):
        """
        Test that the correct template is used.
        """
        self.assertCorrectTemplateUsed('common/home.html')

class DevicesViewTestCase(ViewsTestMixin, TestCase):
    """
    Test case for `views.DevicesView`.
    """
    view_class = views.DevicesView

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
        expected_devices = Device.objects.for_user(self.user).order_by('name')
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
