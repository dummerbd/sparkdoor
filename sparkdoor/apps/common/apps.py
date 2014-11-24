"""
apps.py - contains server side counterparts to device firmware.
"""
from sparkdoor.apps.spark.apps import DeviceAppBase


class DoorApp(DeviceAppBase):
    """
    Device app for `door` firmware.
    """
    action_names = ['open', 'invite', 'stats']
    template_name = 'common/door_app.html'

    def action(self, name, args=None):
        """
        Handle an action request.
        """
        if name in self.action_names and hasattr(self, name):
            return getattr(self, name)(args)

    def open(self, args):
        """
        Ask the device to open.
        """
        pass

    def invite(self, args):
        """
        Invite someone to use this device by sending them a pass.
        """
        pass

    def stats(self, args):
        """
        Return some basic useage stats about this device.
        """
        pass
