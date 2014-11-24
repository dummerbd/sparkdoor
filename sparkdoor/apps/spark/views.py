"""
views.py - `spark` app views module.
"""
from django.views.generic.edit import CreateView

from braces.views import LoginRequiredMixin, FormMessagesMixin

from rest_framework import generics, mixins, response
from rest_framework.permissions import IsAuthenticated

from .forms import RegisterDeviceForm
from .models import Device
from .serializers import DeviceSerializer


class DeviceAPIView(mixins.RetrieveModelMixin, mixins.ListModelMixin,
        generics.GenericAPIView):
    """
    RESTful resource for listing the devices for the current user.

    /device/
        /<id>/
            /<action>/

    The device list and detail endpoints are read-only for now, while
    the action endpoint is write-only and delegates to the device's app.
    """
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Only return the devices for a specific User.
        """
        return Device.objects.for_user(self.request.user)

    @property
    def allowed_methods(self):
        """
        Only GET supported on the device list and detail endpoints, only
        POST supported on the device action endpoint.
        """
        return [('POST' if 'action' in self.kwargs else 'GET'), 'OPTIONS', 'HEAD']

    def list(self, request, *args, **kwargs):
        """
        Add an `href` entry.
        """
        res = super(self.__class__, self).list(request, *args, **kwargs)
        res.data = {
            'href': request.build_absolute_uri(request.path),
            'devices': res.data
        }
        return res

    def get(self, request, *args, **kwargs):
        """
        If the `lookup_url_kwarg` is passed in `kwargs`, then respond
        like a detail view, otherwise respond like a list view.
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in kwargs:
            if 'action' in kwargs:
                return response.Response(status=405)
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Only the command and status endpoints support post for now.
        An additional `action` url kwarg must be specified to know which
        action to perform.

        A 405 is raised if `action` or `pk` is not specified (indicating
        a post to the detail or list endpoints). A 404 is raised if
        `action` is not in the `action_names` attribute.
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg not in kwargs or 'action' not in kwargs:
            return response.Response(status=405)

        action = kwargs['action']
        app = self.get_object().get_app()
        if action not in app.get_action_names():
            return response.Response(status=404)

        return response.Response(data=app.action(action, request.DATA), status=200)


class UserDevicesViewBase(LoginRequiredMixin, FormMessagesMixin, CreateView):
    """
    View base class for listing a user's devices by delegating rendering
    to a `DeviceAppBase` subclass for that device's `app_name`. A new
    device registration form is also provided.

    Subclasses must define the following attributes:
        `template_name` - The template to render.
        `success_url` - Should be the url for this view. This is where
            the user is redirected to after they submit the registration
            form.
    """
    form_class = RegisterDeviceForm
    form_invalid_message = 'Could not register device'

    def get_form_valid_message(self):
        """
        Get the message to display on successfully registering a device.
        """
        return 'Added {0} device'.format(self.object.name)

    def get_context_data(self, **kwargs):
        """
        Add a `devices` entry with available devices.
        """
        context = super(UserDevicesViewBase, self).get_context_data(**kwargs)
        devices = Device.objects.for_user(self.request.user).order_by('name')
        context['devices'] = [d.get_app().render(self.request) for d in devices]
        return context

    def post(self, request, *args, **kwargs):
        """
        Add the user of this request.
        """
        request.POST = request.POST.copy()
        request.POST['user'] = self.request.user.id
        return super(UserDevicesViewBase, self).post(request, *args, **kwargs)
