"""
apps.py - contains classes for building device apps, which are the
    server side counterpart to device firmware.
"""
from django.template.loader import render_to_string
from django.template import RequestContext


class DeviceAppError(Exception):
    """
    Generic device error that can be raised in the `action` function.
    """
    def __init__(self, msg, status_code, *args):
        self.msg = msg
        self.status_code = status_code
        return super(self.__class__, self).__init__(*args)


class DeviceAppBase:
    """
    Base class for Spark device apps. This class is responsible for
    rendering a device in the `UserDevicesViewBase` subclasses and for
    handling `action` requests.

    This class serves as the server side counterpart to the firmware
    running on your spark devices. A `spark.models.Device` instance is
    associated to this app via the `app_name` variable that you must
    provide in your device firmware.

    Use the `APPS` setting in the `SPARK` settings to associate an app
    name with a subclass of `DeviceAppBase`.
    """
    action_names = []

    def __init__(self, device):
        """
        Constructor.
        """
        self.device = device

    def get_action_names(self):
        """
        Get the action names available from this app. These values
        should be recognized by the `action` function.

        By default, returns the `action_names` attribute.
        """
        return self.action_names

    def action(self, name, args=None):
        """
        Handle an action request.
        """
        raise NotImplementedError

    def get_context_data(self):
        """
        Get the context data for rendering this app's template.
        """
        return {'device': self.device}

    def render(self, request):
        """
        Render this device as HTML.
        """
        self.request = request
        context = RequestContext(request, self.get_context_data())
        return render_to_string(self.template_name, context_instance=context)


class DefaultDeviceApp(DeviceAppBase):
    """
    This class does not provide any functionality, it is used if a
    device is registered that has an `app_name` that is not recognized.
    """
    action_names = []

    def action(self, name, args=None):
        """
        Do nothing.
        """
        pass

    def render(self, request):
        """
        Render this device as HTML.
        """
        return '<p>App: {0}<br>Name: {1}</p>'.format(self.device.app_name,
            self.device.name)
