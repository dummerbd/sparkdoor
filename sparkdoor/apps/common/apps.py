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
    action_names = ['open', 'pair_id_card']
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

    def pair_id_card(self, args):
        """
        Read an ID card and pair it with this device.
        """
        try:
            success = self.device.call("pair_id_card", None) == 0
            uid = self.device.read("card_uid") if success else None
        except ServiceError as err:
            raise DeviceAppError('Device could not be reached', err.status_code)
        if not success:
            raise DeviceAppError('Card read timed out', 408)
        name = args.get('name', None) if args else None
        IDCard(device=self.device.id, uid=uid, name=name)
