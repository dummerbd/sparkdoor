"""
models.py - `spark` app models module.
"""
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone

from .services import SparkCloud, CloudDevice, ServiceError
from .settings import SparkSettings


class CloudCredentialsManager(models.Manager):
    """
    Custom model manager for `CloudCredentials`.
    """
    def cloud_service(self):
        """
        Get a cloud service instance initialized with the most current
        credentials.
        """
        latest = self._latest()
        if latest is None:
            return None
        return SparkCloud(SparkSettings().API_URI, latest.access_token)

    def _access_token(self):
        """
        Get the most recent valid `access_token`, if one isn't found
        then None is returned.
        """
        latest = self._latest()
        if latest is None:
            return None
        return latest.access_token

    def refresh_token(self):
        """
        Check if the access token will expire soon, if so then attempt
        to find any existing tokens on the cloud account. If no existing
        tokens are found then a new one will be requested.
        """
        latest = self._latest()
        if latest is None or latest.expires_soon():
            cloud = SparkCloud(SparkSettings().API_URI)
            self._discover_tokens(cloud)
            if self._access_token() is None:
                self._renew_token(cloud)

    def _renew_token(self, cloud):
        """
        Get a new token from the cloud service and record it.
        """
        s = SparkSettings()
        token, expires_at = cloud.renew_token(s.USERNAME, s.PASSWORD)
        CloudCredentials(access_token=token, expires_at=expires_at).save()

    def _discover_tokens(self, cloud):
        """
        Get existing tokens from the cloud service and save the most
        recent.
        """
        s = SparkSettings()
        token, expires_at = cloud.discover_tokens(s.USERNAME, s.PASSWORD)
        if (token is not None and expires_at is not None and
                not self.filter(access_token=token).exists()):
            CloudCredentials(access_token=token, expires_at=expires_at).save()

    def _latest(self):
        """
        Get the latest valid credentials or return None.
        """
        try:
            return self.get_queryset().filter(
                    expires_at__gt=timezone.now()
                ).latest(
                    'expires_at'
                )
        except CloudCredentials.DoesNotExist:
            return None


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


class DeviceManager(models.Manager):
    """
    Custom query set for `Device` model.
    """
    def for_user(self, user):
        """
        Get a list of devices for a user.
        """
        return self.filter(user=user)

    def by_name(self, user, name):
        """
        Get a device for a given device name.
        """
        return self.for_user(user).get(name=name)

    def by_device_id(self, user, id):
        """
        Get a device by an id.
        """
        return self.for_user(user).get(device_id=id)


class Device(models.Model):
    """
    Stores information about a Spark device.
    """
    device_id = models.CharField(max_length=250, blank=False, unique=True)
    name = models.CharField(max_length=250, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)
    app_name = models.CharField(max_length=100, blank=False, default='default')

    objects = DeviceManager()

    class Meta:
        unique_together = ('name', 'user')

    def call(self, func_name, func_args):
        """
        Call a function on this device and return the result which will
        always be an integer for a successfull call.
        """
        return self._cloud_device.call(func_name, func_args)
    call.do_not_call_in_templates = True

    def read(self, var_name):
        """
        Read the value of a variable.
        """
        return self._cloud_device.read(var_name)

    def get_app(self):
        """
        Use the `APPS` entry in the `SPARK` settings to get a
        `spark.views.DeviceAppBase` subclass for this device.
        """
        app_class = SparkSettings().APPS.get(self.app_name, SparkSettings().DEFAULT_APP)
        return app_class(self)

    @property
    def variables(self):
        """
        The available variables for this device as a dictionary mapping
        a name to a type (either 'int32', 'string', or 'double').
        """
        return self._cloud_device.variables

    @property
    def functions(self):
        """
        The available functions for this device in a list.
        """
        return self._cloud_device.functions

    @property
    def _cloud_device(self):
        """
        Get a `CloudDevice` instance from the Spark cloud and cache it.
        """
        if not hasattr(self, '_cached_cloud_device'):
            cloud = CloudCredentials.objects.cloud_service()
            self._cached_cloud_device = cloud.device(self.device_id)
        if self._cached_cloud_device is None:
            raise ServiceError(502)
        return self._cached_cloud_device
