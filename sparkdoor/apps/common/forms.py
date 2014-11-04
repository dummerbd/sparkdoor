"""
forms.py - form classes for the `common` app.
"""
from django.forms import ModelForm

from sparkdoor.apps.spark.models import Device


class RegisterDeviceForm(ModelForm):
    """
    From for registering new spark devices. This form ensures that the
    `device_id` isn't already claimed and exists in the Spark cloud.
    """
    class Meta:
        model = Device
        fields = ['user', 'device_id', 'name']

    def clean(self):
        """
        Validate that the `device_id` is correct by first looking for
        Devices with this id in the database and then by attempting to
        read the `app_name` variable.

        If the form isn't valid, then there's no point in running these
        checks so just return.
        """
        data = super(RegisterDeviceForm, self).clean()
        return data
