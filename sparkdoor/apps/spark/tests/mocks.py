"""
mocks.py - reusable mock classes.
"""
import os
import json

from httmock import response, urlmatch

from ..settings import SparkSettings


HEADERS = {
    'content-type': 'application/json'
}
NETLOC = '^{0}$'.format(SparkSettings().API_URI)
RESPONSE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api.spark.io')
GET = 'get'
POST = 'post'
PUT = 'put'
DELETE = 'delete'


class Resource:
    """
    An arbitrary REST resource that maps to the file system. Only
    supports GET (file reads) for now.
    """
    class Resource404(Exception):
        """
        File could not be found, etc.
        """
        pass

    def __init__(self, path):
        """
        Map a resource uri path to a file.
        """
        self.path = os.path.join(RESPONSE_DIR, '{0}.json'.format(path))

    def get(self):
        """
        Respond to a GET request.
        """
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except:
            raise Resource.Resource404


@urlmatch(netloc=NETLOC)
def spark_cloud_mock(path, request):
    """
    Use with `httmock.with_httmock` decorator or `httmock.HttMock`
    context manager.

    This mock emulates the v1 REST api for the Spark cloud service by
    mapping request paths to the json files and directories stored in
    the `api.spark.io` directory. The contents of these files are simply
    returned as the response content. If a path is not found then a 404
    is returned.

    Note: this mock will respect the `SPARK.CLOUD_API_URI` setting in
    request paths.
    """
    pass
