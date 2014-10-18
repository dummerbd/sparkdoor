"""
services.py - module for interacting with a Spark cloud service.
"""
from hammock import Hammock

from .settings import SparkSettings


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

    def __init__(self, access_token=None):
        """
        Instances a new web service using the path in
        `SparkSettings.API_URI`. An `access_token` can be specified if
        one has already been granted.
        """
        self._settings = SparkSettings()
        self._service = Hammock(self._settings.API_URI)
        if access_token is not None:
            self.access_token = access_token
        else:
            self._login()

    def _login(self, username=None, password=None):
        """
        Will attempt to get a new access_token from the cloud service
        using `SparkSettings.USERNAME` and `SparkSettings.PASSWORD` or
        the passed in `username` and `password`.

        An invalid login will return None, otherwise the access token is
        returned, which also sets the `access_token` attribute.
        """
        username = username or self._settings.USERNAME
        password = password or self._settings.PASSWORD
        auth = ('spark', 'spark')
        data = {
            'grant_type': 'password',
            'username': username,
            'password': password
        }
        response = self._service.oauth.token.POST(auth=auth, data=data)
        self.access_token = response.json().get('access_token') if response.ok else None

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
