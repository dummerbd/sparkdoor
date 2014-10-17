"""
mocks.py - reusable mock classes.
"""
import os
import json

from sparkdoor.libs.httmock import response, all_requests

from ..settings import SparkSettings


HEADERS = {
    'content-type': 'application/json; charset=utf-8'
}
RESPONSE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api.spark.io')
GET = 'get'
POST = 'post'
PUT = 'put'
DELETE = 'delete'


def resource(path, request):
    """
    A plain REST resource that maps to response content stored in JSON
    files.
    """
    res = response(404, {}, HEADERS, None, 5, request)
    path = path if path[0] != '/' else path[1:]
    file_path = os.path.join(RESPONSE_DIR, '{0}.json'.format(path))
    try:
        with open(file_path, 'r') as f:
            content = json.load(f)
        res = response(200, content, HEADERS, None, 5, request)
    except:
        pass
    return res


def oauth_request_is_valid(request):
    """
    Check that a request is valid and should be granted a token.
    """
    r = request.original
    ss = SparkSettings()
    return (r.method.lower() == POST and r.auth == ('spark', 'spark') and
        r.data['username'] == ss.USERNAME and r.data['password'] == ss.PASSWORD and
        r.data['grant_type'] == 'password')


def oauth_token(path, request):
    """
    Respond to the `/oauth/token` resource, which grants access tokens
    from valid login credentials. Any malformed requests, including
    invalid credentials, returns a 400 response.
    """
    res = response(400, {}, HEADERS, None, 5, request)
    if oauth_request_is_valid(request):
        res = resource(path, request)
    return res


HANDLERS = {
    '/oauth/token': oauth_token
}


@all_requests
def spark_cloud_mock(url_split, request):
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
    path = url_split.path
    return HANDLERS.get(path, resource)(path, request)
