"""
models.py - `spark` app models module.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone

from .services import SparkCloud


class CloudCredentialsManager(models.Manager):
    """
    Custom model manager for `CloudCredentials`.
    """
    def access_token(self):
        """
        Get the most recent valid `access_token`, if one isn't found
        then None is returned.
        """
        try:
            return self.get_queryset().filter(
                expires_at__gt=timezone.now()
            ).latest(
                'expires_at'
            ).access_token
        except:
            return None


class CloudCredentials(models.Model):
    """
    Stores credentials to access a Spark cloud service.
    """
    access_token = models.CharField(max_length=250, blank=False)
    expires_at = models.DateTimeField()

    objects = CloudCredentialsManager()


class Device(models.Model):
    """
    Stores information about a Spark device.
    """
    device_id = models.IntegerField(null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)
