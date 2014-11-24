"""
test_apps.py - test cases for the `spark` app's app module.
"""
from django.test import SimpleTestCase

from .. import apps


class DeviceAppBaseTestCase(SimpleTestCase):
    """
    Test case for `apps.DeviceAppBase`.
    """
    app_class = apps.DeviceAppBase

    def test_get_action_names(self):
        """
        Test that `get_action_names` returns the `action_names`
        atrribute.
        """
        app = type('TestApp', (self.app_class,), {'action_names': ['action']})(None)
        self.assertEqual(app.get_action_names(), app.action_names)

    def test_get_context_data(self):
        """
        Test that `get_context_data` includes a `device` entry.
        """
        app = self.app_class('a device')
        context = app.get_context_data()
        self.assertEqual(context['device'], app.device)
