"""
serializers.py - `spark` app serializers module.
"""
from rest_framework import serializers

from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for exposing the `Device` model as a REST resource.
    """
    class Meta:
        model = Device
        fields = ('id', 'name', 'app_name')
