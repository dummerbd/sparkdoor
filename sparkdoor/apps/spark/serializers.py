"""
serializers.py - `spark` app serializers module.
"""
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for exposing the `Device` model as a REST resource.
    """
    href = serializers.SerializerMethodField('get_self_uri')

    actions = serializers.SerializerMethodField('get_actions')

    class Meta:
        model = Device
        fields = ('id', 'name', 'app_name', 'href', 'actions')

    def get_self_uri(self, obj):
        """
        Get the `uri` for this device.
        """
        if obj.id is None:
            return ''
        return reverse('devices-detail', kwargs={'pk': obj.id}, 
            request=self.context['request'])

    def get_actions(self, obj):
        """
        Get a list of available actions and their uris.
        """
        href = lambda a: reverse('devices-action', kwargs={'pk': obj.id, 'action': a},
            request=self.context['request'])
        return [{'href': href(a), 'name': a} for a in obj.get_app().get_action_names()]
