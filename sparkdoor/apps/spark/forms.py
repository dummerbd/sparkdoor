"""
forms.py - form classes for the `common` app.
"""
from django import forms

from .services import ServiceError
from .models import CloudCredentials, Device


class RegisterDeviceForm(forms.ModelForm):
    """
    From for registering new spark devices. This form ensures that the
    `device_id` isn't already claimed and exists in the Spark cloud.
    """
    class Meta:
        model = Device
        fields = ['user', 'device_id', 'name', 'app_name']

    app_name = forms.CharField(required=False)

    def _get_app_name(self, device):
        """
        Attempt to get the `app_name` variable from a cloud device.
        """
        try:
            return device.read('app_name')
        except ServiceError:
            self.add_error('device_id', 'This device could not be reached.')
        return None

    def clean(self):
        """
        Validate that the `device_id` is correct by first looking for
        Devices with this id in the database and then by attempting to
        read the `app_name` variable.
        """
        data = super(RegisterDeviceForm, self).clean()
        device_id = data.get('device_id', None)

        if device_id and not Device.objects.filter(device_id=device_id).exists():
            device = CloudCredentials.objects.cloud_service().device(device_id)
            if device is None:
                self.add_error('device_id', 'This device id is invalid.')
            else:
                data['app_name'] = self._get_app_name(device)
        return data
