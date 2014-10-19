"""
models.py - `spark` app models module.
"""
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone

from .services import SparkCloud
from .settings import SparkSettings


class CloudCredentialsManager(models.Manager):
    """
    Custom model manager for `CloudCredentials`.
    """
    def access_token(self):
        """
        Get the most recent valid `access_token`, if one isn't found
        then None is returned.
        """
        cred = None
        try:
            cred = self.get_queryset().latest('expires_at')
        except CloudCredentials.DoesNotExist:
            pass
        if cred and cred.is_valid():
            return cred.access_token
        return None

    def renew_token(self):
        """
        Get a new token from the cloud service, save it in a new record,
        and return it.
        """
        token, expires_at = SparkCloud().renew_token()
        CloudCredentials(access_token=token, expires_at=expires_at).save()
        return token


class CloudCredentials(models.Model):
    """
    Stores credentials to access a Spark cloud service.
    """
    access_token = models.CharField(max_length=250, blank=False)
    expires_at = models.DateTimeField()

    def is_valid(self):
        """
        Determine if these credentials are still within the exipiration
        date.
        """
        window = SparkSettings().RENEW_TOKEN_WINDOW
        return self.expires_at > (timezone.now() + timedelta(seconds=window))

    objects = CloudCredentialsManager()


class Device(models.Model):
    """
    Stores information about a Spark device.
    """
    device_id = models.IntegerField(null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)
