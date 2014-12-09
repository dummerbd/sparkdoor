"""
apps.py - contains server side counterparts to device firmware.
"""
from sparkdoor.apps.spark.apps import DeviceAppBase, DeviceAppError
from sparkdoor.apps.spark.services import ServiceError


from .models import IDCard


class DoorApp(DeviceAppBase):
    """
    Device app for `door` firmware.
    """
    action_names = ['open', 'idcard']
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
        try:
            self.device.call("open", None)
        except ServiceError as err:
            raise DeviceAppError('Device could not be reached', err.status_code)

    def idcard(self, args):
        """
        Attempt to open using an ID card.
        """
        try:
            uid = args['uid']
        except:
            raise DeviceAppError('Request must include a "uid" entry in POST data.', 400)
        id_card = self.device.idcard_set.filter(uid=uid)
        if len(id_card) > 0:
            self.open({})
        else:
            raise DeviceAppError('UID was invalid.', 403)

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
