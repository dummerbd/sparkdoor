"""
apps.py - contains server side counterparts to device firmware.
"""
from sparkdoor.apps.spark.apps import DeviceAppBase


class DoorApp(DeviceAppBase):
    """
    Device app for `door` firmware.
    """
    action_names = ['open']
    template_name = 'common/door_app.html'

    def action(self, name, args=None):
        """
        Handle an action request.
        """
        pass
