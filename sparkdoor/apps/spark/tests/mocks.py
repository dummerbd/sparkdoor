"""
mocks.py - reusable mock classes.
"""
import os
import json
from datetime import timedelta, datetime

from sparkdoor.libs.httmock import response, all_requests

from ..settings import SparkSettings
from ..services import CLOUD_DATETIME_FORMAT


HEADERS = {
    'content-type': 'application/json; charset=utf-8'
}
RESPONSE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api.spark.io')
ACCESS_TOKEN = '12345abcde'
GET = 'get'
POST = 'post'
PUT = 'put'
DELETE = 'delete'


def resource(path, request, check_token=True):
    """
    A plain REST resource that maps to response content stored in JSON
    files.
    """
    res = response(404, {}, HEADERS, None, 5, request)
    if check_token and request.original.params.get('access_token') != ACCESS_TOKEN:
        res = response(400, {}, HEADERS, None, 5, request)
    else:
        path = path if path[0] != '/' else path[1:]
        file_path = os.path.join(RESPONSE_DIR, '{0}.json'.format(path))
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
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
        res = resource(path, request, False)
        c = json.loads(res._content.decode('utf-8'))
        c['access_token'] = ACCESS_TOKEN
        res._content = bytes(json.dumps(c), 'utf-8')
    return res


def valid_credentials(request):
    """
    Check the credentials.
    """
    username, password = request.original.auth
    s = SparkSettings()
    return s.USERNAME == username and s.PASSWORD == password


def v1_access_tokens(path, request):
    """
    Respond to the `/v1/access_tokens` resource, which lists active
    tokens on GET.
    """
    res = response(400, {}, HEADERS, None, 5, request)
    if request.method.lower() == GET and valid_credentials(request):
        res = resource(path, request, False)
        c = json.loads(res._content.decode('utf-8'))
        # the first token is the most recent valid entry
        c[0]['token'] = ACCESS_TOKEN
        c[0]['expires_at'] = (datetime.now() + timedelta(days=90)).strftime(
            CLOUD_DATETIME_FORMAT)
        # the second token is old
        c[1]['expires_at'] = (datetime.now() + timedelta(days=1)).strftime(
            CLOUD_DATETIME_FORMAT)
        res._content = bytes(json.dumps(c), 'utf-8')
    return res


def valid_func_token(request):
    """
    Check that a valid access token was used with a function request.
    """
    return request.original.data.get('access_token', None) == ACCESS_TOKEN


def device_func(path, request):
    """
    Respond to the `/v1/devices/<device_id>/<func>` resource which 
    represents a function call.
    """
    res = response(400, {}, HEADERS, None, 5, request)
    if request.method.lower() == POST and valid_func_token(request):
        return resource(path, request, False)


def device_var(path, request):
    """
    Respond to the `/v1/devices/<device_id>/<var>` resource which 
    represents a variable.
    """
    res = response(400, {}, HEADERS, None, 5, request)
    if request.method.lower() == GET:
        res = resource(path, request)
        if res.status_code == 200:
            c = json.loads(res._content.decode('utf-8'))
            c['coreInfo']['last_heard'] = datetime.now().strftime(CLOUD_DATETIME_FORMAT)
            res._content = c
    return res


HANDLERS = [
    ('/oauth/token', oauth_token),
    ('/v1/access_tokens', v1_access_tokens),
    ('/v1/devices/12345abcde12345abcde/func', device_func),
    ('/v1/devices/12345abcde12345abcde/', device_var)
]


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
    for p, handler in HANDLERS:
        if path.startswith(p):
            return handler(path, request)
    return resource(path, request)
