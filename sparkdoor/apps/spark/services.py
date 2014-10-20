"""
services.py - module for interacting with a Spark cloud service.
"""
from datetime import timedelta

from django.utils import timezone

from hammock import Hammock


class SparkCloud:
    """
    Interface to interacting with a Spark cloud web service with lazy
    evaluation. Requests to the Spark cloud are sent on demand and
    cached.
    """
    class Device:
        """
        Represents a Spark core device.
        """
        def __init__(self, cloud, **kwargs):
            """
            Copy `kwargs` onto instance.
            """
            self.cloud = cloud
            self.name = None
            self.id = None
            self.connected = None
            self.last_app = None
            self.last_heard = None
            [setattr(self, k, v) for k, v in kwargs.items()]

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

        @property
        def variables(self):
            return self._extra.get('variables', {})

        @property
        def functions(self):
            return self._extra.get('functions', [])

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

    @property
    def devices(self):
        """
        Get the available Spark cores from this access token.
        """
        if self.access_token is None:
            return []
        response = self._service.v1.devices.GET(params={'access_token': self.access_token})
        if response.ok:
            devices = response.json()
            return [SparkCloud.Device(self, **d) for d in devices]
        return []
