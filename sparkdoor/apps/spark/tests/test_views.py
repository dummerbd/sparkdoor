"""
test_views.py - test cases for the `spark` app's view module.
"""
from django.test import TestCase, override_settings
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured

from rest_framework.response import Response

from sparkdoor.libs.httmock import HTTMock
from sparkdoor.libs.testmixins import ViewsTestMixin, APITestMixin
from sparkdoor.libs.factories import UserFactory

from .factories import DeviceFactory, CloudCredentialsFactory
from .mocks import spark_cloud_mock, ACCESS_TOKEN
from .. import views, models, apps
 

class TestApp(apps.DeviceAppBase):
    action_names = ['test_action']
    def action(self, name, args):
        return 'some_data'


spark_test_settings = {
    'CLOUD_USERNAME': 'a_user',
    'CLOUD_PASSWORD': 'password',
    'CLOUD_API_URI': 'https://api.test.com',
    'CLOUD_RENEW_TOKEN_WINDOW': 60*60, # 1 hour
    'APPS': { 'test_app': TestApp }
}


@override_settings(SPARK=spark_test_settings)
class DeviceAPIViewTestCase(APITestMixin, TestCase):
    """
    Test case for `views.DeviceAPIView`.
    """
    view_class = views.DeviceAPIView

    @classmethod
    def setUpClass(cls):
        """
        Add a test device.
        """
        cls.user = UserFactory.create()
        cls.device = DeviceFactory.create(user=cls.user, app_name='test_app')

    def test_get_list(self):
        """
        Test that `get` calls `list` when a lookup kwarg is not given.
        """
        class TestView(self.view_class):
            def list(self, *args, **kwargs):
                return Response('list data')

        response = self.send_request_to_view(method='GET', view_class=TestView)
        self.assertEqual(response.data, 'list data')

    def test_get_retrieve(self):
        """
        Test that `get` calls `retrieve` when a lookup kwarg is given.
        """
        class TestView(self.view_class):
            def retrieve(self, *args, **kwargs):
                return Response('object data')

        response = self.send_request_to_view(method='GET', view_class=TestView, 
            kwargs={'pk': self.device.id})
        self.assertEqual(response.data, 'object data')

    def test_post_no_pk(self):
        """
        Test that `post` raises ImproperlyConfigured when the `pk` kwarg
        isn't specified.
        """
        with self.assertRaises(ImproperlyConfigured):
            self.send_request_to_view(method='POST', kwargs={})

    def test_post_no_action(self):
        """
        Test that `post` raises a 404 when the `action` kwarg isn't
        specified.
        """
        response = self.send_request_to_view(method='POST',
            kwargs={'pk': self.device.id})
        self.assertEqual(response.status_code, 404)

    def test_post_invalid_action(self):
        """
        Test that `post` raises a 404 when the `action` kwarg is not in
        the app's `action_names` attribute.
        """
        response = self.send_request_to_view(method='POST',
            kwargs={'pk': self.device.id, 'action': 'not an action name'})
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        """
        Test that `post` calls an app's `action` function with the
        `action` kwarg and the post data.
        """
        response = self.send_request_to_view(method='POST',
            kwargs={'pk': self.device.id, 'action': 'test_action'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'some_data')


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
