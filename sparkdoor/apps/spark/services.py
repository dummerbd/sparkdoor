"""
services.py - module for interacting with a Spark cloud service.
"""
from datetime import timedelta, datetime

from django.utils import timezone

from hammock import Hammock


CLOUD_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class ServiceError(Exception):
    """
    Generic service error.
    """
    pass


class SparkCloud:
    """
    Interface to interacting with a Spark cloud web service with lazy
    evaluation. Requests to the Spark cloud are sent on demand and
    cached.
    """
    def __init__(self, api_uri, access_token=None):
        """
        Instances a new web service using the path in `api_uri`. An 
        `access_token` can be specified if one has already been granted.
        """
        self._service = Hammock(api_uri)
        self.access_token = access_token

    def renew_token(self, username, password):
        """
        Will attempt to get a new access_token from the cloud service
        using `username` and `password`.

        An invalid login will return the tuple (None, None) otherwise a
        tuple (access_token, expires_by) is returned and the
        `access_token` attribute is set.
        """
        self.access_token = None
        expires_at = None
        data = {'grant_type': 'password', 'username': username, 'password': password}
        response = self._service.oauth.token.POST(auth=('spark', 'spark'), data=data)
        if response.ok:
            d = response.json()
            self.access_token = d['access_token']
            expires_at = timezone.now() + timedelta(seconds=int(d['expires_in']))
        return (self.access_token, expires_at)

    def discover_tokens(self, username, password):
        """
        Will attempt to find any tokens already active on this account.
        If any are found, the most recent token will be returned in a
        tuple (access_token, expires_by) and the `access_token`
        attribute is set, otherwise (None, None) is returned.
        """
        token, expires_at = None, None
        response = self._service.v1.access_tokens.GET(auth=(username, password))
        if response.ok:
            for entry in response.json():
                entry['expires_at'] = datetime.strptime(entry['expires_at'],
                    CLOUD_DATETIME_FORMAT)
                if expires_at is None or entry['expires_at'] > expires_at:
                    expires_at = entry['expires_at']
                    token = entry['token']
                    self.access_token = token
        return (token, expires_at)

    def all_devices(self):
        """
        Get the available Spark cores from this access token.
        """
        if self.access_token is None:
            return []
        response = self._service.v1.devices.GET(params={'access_token': self.access_token})
        if response.ok:
            devices = response.json()
            return [CloudDevice(self, **d) for d in devices]
        return []

    def device(self, device_id):
        """
        Get an available Spark core for a given device id.
        """
        if self.access_token is None:
            return []
        response = self._service.v1.devices.GET(device_id, params={'access_token': self.access_token})
        if response.ok:
            device = response.json()
            cloud_device = CloudDevice(self, **device)
            cloud_device._extra = device
            return cloud_device
        return None


class CloudDevice:
    """
    Represents a Spark cloud device.
    """
    def __init__(self, cloud, id=None, name=None, connected=True, last_heard=None, **kwargs):
        """
        Constructor.
        """
        self.cloud = cloud
        self.name = name
        self.id = id
        self.connected = connected
        self.last_heard = last_heard
        self.last_app = None

    @property
    def _extra(self):
        """
        Get extra info from the cloud when requested. Result is
        cached.
        """
        if not hasattr(self, '_extra_cached'):
            response = self.cloud._service.v1.devices.GET(self.id,
                params={'access_token':self.cloud.access_token})
            self._extra_cached = response.json() if response.ok else {}
        return self._extra_cached

    @_extra.setter
    def _extra(self, value):
        """
        Allows pre-initializing extra info.
        """
        self._extra_cached = value

    def call(self, func_name, func_args):
        """
        Call a function on this device and return the result which will
        always be an integer for a successful call. An unsuccessful call
        will raise a `ServiceError`.
        """
        func_args = str(func_args)
        response = self.cloud._service.v1.devices.POST(self.id, func_name,
            data={'access_token':self.cloud.access_token, 'args':func_args})
        if response.ok:
            return response.json()['return_value']
        raise ServiceError(response.status_code)

    def read(self, var_name):
        """
        Read the value of a variable. An unsuccessful read will raise a
        `ServiceError`.
        """
        response = self.cloud._service.v1.devices.GET(self.id, var_name,
            params={'access_token':self.cloud.access_token})
        if response.ok:
            return response.json()['result']
        raise ServiceError(response.status_code)

    @property
    def variables(self):
        """
        The available variables for this device as a dictionary mapping
        a name to a type (either 'int32', 'string', or 'double').
        """
        return self._extra.get('variables', {})

    @property
    def functions(self):
        """
        The available functions for this device in a list.
        """
        return self._extra.get('functions', [])
