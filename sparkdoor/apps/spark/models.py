"""
models.py - `spark` app models module.
"""
from django.db import models
from django.conf import settings


class CloudCredentials(models.Model):
    """
    Stores credentials to access a Spark cloud service.
    """
    access_token = models.CharField(max_length=250, blank=False)
    expires_at = models.DateTimeField()


class Device(models.Model):
    """
    Stores information about a Spark device.
    """
    device_id = models.IntegerField(null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)
