"""
test_serializers.py - test cases for the `spark` app's serializers
    module.
"""
from django.test import SimpleTestCase, override_settings
from django.conf.urls import patterns, url

from rest_framework.test import APIRequestFactory, force_authenticate

from .factories import DeviceFactory
from .. import serializers, apps


urlpatterns = patterns('',
    url(r'^devices/(?P<pk>\d+)/$', 'fake_view', name='devices-detail'),
    url(r'^devices/(?P<pk>\d+)/(?P<action>[\w\d\-]+)/$', 'fake_view',
        name='devices-action')
)


class TestApp(apps.DeviceAppBase):
    action_names = ['test-action']


spark_test_settings = {
    'CLOUD_USERNAME': 'a_user',
    'CLOUD_PASSWORD': 'password',
    'APPS': { 'test_app': TestApp }
}


@override_settings(SPARK=spark_test_settings)
class DeviceSerializerTestCase(SimpleTestCase):
    """
    Test case for `serializers.DeviceSerializer`.
    """
    urls = __name__

    def test_serialize(self):
        """
        Test that the correct fields are serialized including a `self`
        uri link.
        """
        device = DeviceFactory.build(id=1, app_name='test_app')
        context = {'request': APIRequestFactory().get(path='', user=device.user)}
        serializer = serializers.DeviceSerializer(device, context=context)
        expected_data = {
            'id': device.id,
            'name': device.name,
            'app_name': device.app_name,
            'href': 'http://testserver/devices/1/',
            'actions': [
                { 'name': 'test-action',
                  'href': 'http://testserver/devices/1/test-action/'}
            ]
        }
        self.assertEqual(expected_data, serializer.data)
