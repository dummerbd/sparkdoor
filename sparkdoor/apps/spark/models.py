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
        then a new one is granted.
        """
        now = timezone.now()
        try:
            token = self.get_queryset().filter(
                expires_at__gt=now
            ).latest(
                'expires_at'
            ).access_token
        except:
            cloud = SparkCloud()
            token = cloud.access_token
            CloudCredentials(access_token=token, expires_at=cloud.expires_at)
        return token


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
