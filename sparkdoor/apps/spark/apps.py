"""
apps.py - `spark` app apps module.
"""
class DeviceAppBase:
    """
    Base class for Spark device apps. This class is responsible for
    rendering a device in the `UserDevicesViewBase` subclasses and for
    handling `command` and `status` requests.

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

    def render(self):
        """
        Render this device as HTML.
        """
        raise NotImplementedError


class DefaultDeviceApp(DeviceAppBase):
    """
    This class does not provide any functionality, it is used if a
    device is registered that has an `app_name` that is not recognized.
    """
    pass
