"""
test_views.py - test cases for the `common` app's view module.
"""
from django.test import SimpleTestCase, TestCase

from sparkdoor.libs.testmixins import ViewsTestMixin
from sparkdoor.libs.factories import UserFactory
from sparkdoor.apps.spark.models import Device
from sparkdoor.apps.spark.tests.factories import DeviceFactory

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
        print(cls.devices)

    def test_context_data(self):
        """
        Test that the `context` includes a `devices` entry.
        """
        response = self.send_request_to_view()
        context = response.context_data
        expected_devices = Device.objects.for_user(self.user).order_by('name')
        for i, device in enumerate(expected_devices):
            self.assertEqual(device.id, context['devices'][i].id)
