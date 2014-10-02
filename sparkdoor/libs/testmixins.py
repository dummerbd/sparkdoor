"""
testmixins.py - contains mixin classes for various test cases.
"""
from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory

from rest_framework.test import APIRequestFactory, force_authenticate


class CBVBaseTestMixin:
    """
    Class-based views testcase mixin that makes using request factories
    easier.
    """
    view_class = None

    def build_request(self, method='GET', path='/test/', user=None, data=None, **kwargs):
        """
        Creates a request using request factory.
        """
        verb_fn = getattr(self.request_factory, method.lower())
        user = user or self.get_user()
        data = data or {}
        request = verb_fn(path=path, data=data, **kwargs)
        request.user = user
        return request

    def get_user(self):
        """
        Get a user for all test requests.
        """
        return getattr(self, 'user', None) or AnonymousUser()

    def build_view(self, request, args=None, kwargs=None, view_class=None,
            **viewkwargs):
        """
        Creates a `view_class` view instance.
        """
        args = args or ()
        kwargs = kwargs or {}
        view_class = view_class or self.view_class
        return view_class(
            request=request, args=args, kwargs=kwargs, **viewkwargs)

    def dispatch_view(self, request, args=None, kwargs=None, view_class=None,
            **viewkwargs):
        """
        Creates and dispatches `view_class` view.
        """
        view = self.build_view(request, args, kwargs, view_class, **viewkwargs)
        return view.dispatch(request, *view.args, **view.kwargs)

    def send_request_to_view(self, method='GET', path='/test/', user=None, data=None, **kwargs):
        """
        Creates a request and sends it to the `dispatch` method of the
        view and returns the resulting response.
        """
        request = self.build_request(method, path, user, data, **kwargs)
        return self.dispatch_view(request, **kwargs)


class ViewsTestMixin(CBVBaseTestMixin):
    """
    Testcase mixin using Django's `RequestFactory`.
    """
    request_factory = RequestFactory()

    def assertCorrectTemplateUsed(self, template_name, user=None, *args, **kwargs):
        """
        Assert that a GET request with a valid user returns the correct
        template and that the request is OK.
        """
        response = self.send_request_to_view(user=user, *args, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)


class APITestMixin(CBVBaseTestMixin):
    """
    Testcase mixin using Django Rest Framework's `APIRequestFactory`.
    """
    request_factory = APIRequestFactory()

    def buildRequest(self, method='GET', path='/test/', user=None,
            token=None, **kwargs):
        """
        Creates a request using request factory.
        """
        request = super(APITestMixin, self).build_request(method=method, path=path,
            user=user, token=token, **kwargs)
        force_authenticate(request, user=user, token=token)
        return request

    def assertRendersTemplate(self, response, template_name):
        """
        Assert that the response object will render with the correct
        template.
        """
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, template_name)
