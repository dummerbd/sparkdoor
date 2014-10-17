"""
services.py - module for interacting with a Spark cloud service.
"""
from hammock import Hammock

from .settings import SparkSettings


class SparkCloud:
    """
    Interface to interacting with a Spark cloud web service.
    """
    def __init__(self, access_token=None):
        """
        Constructer - instances a new web service using the path in
        `SparkSettings.API_URI`. An `access_token` can be specified if
        one has already been granted.
        """
        self._settings = SparkSettings()
        self._service = Hammock(self._settings.API_URI)
        self.access_token = access_token

    def login(self, username=None, password=None):
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
        if response.ok:
            self.access_token = response.json().get('access_token')
        return self.access_token
