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
        try:
            return self._latest().access_token
        except CloudCredentials.DoesNotExist:
            return None

    def renew_token(self):
        """
        Get a new token from the cloud service, save it in a new record,
        and return it.
        """
        s = SparkSettings()
        renew = True
        try:
            cred = self._latest()
            token = cred.access_token
            renew = cred.expires_soon()
        except:
            pass
        if renew:
            token, expires_at = SparkCloud(s.API_URI).renew_token(s.USERNAME, s.PASSWORD)
            CloudCredentials(access_token=token, expires_at=expires_at).save()
        return token

    def discover_tokens(self):
        """
        Attempt to retrieve existing tokens from the cloud service, save
        the most recent in a new record if needed, and return it.
        """
        s = SparkSettings()
        token, expires_at = SparkCloud(s.API_URI).discover_tokens(s.USERNAME, s.PASSWORD)
        if (token is not None and expires_at is not None and
                not self.filter(access_token=token).exists()):
            CloudCredentials(access_token=token, expires_at=expires_at).save()
        return token

    def _latest(self):
        return self.get_queryset().filter(
                expires_at__gt=timezone.now()
            ).latest(
                'expires_at'
            )


class CloudCredentials(models.Model):
    """
    Stores credentials to access a Spark cloud service.
    """
    access_token = models.CharField(max_length=250, blank=False, unique=True)
    expires_at = models.DateTimeField()

    def expires_soon(self):
        """
        Determine if these credentials are still within the exipiration
        date.
        """
        window = SparkSettings().RENEW_TOKEN_WINDOW
        return self.expires_at <= (timezone.now() + timedelta(seconds=window))

    objects = CloudCredentialsManager()


class Device(models.Model):
    """
    Stores information about a Spark device.
    """
    device_id = models.CharField(max_length=250, blank=False)
    name = models.CharField(max_length=250, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)

    class Meta:
        unique_together = ('name', 'user')
