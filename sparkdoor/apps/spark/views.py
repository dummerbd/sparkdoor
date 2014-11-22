"""
views.py - `spark` app views module.
"""
from django.http import Http404
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
    REST api viewset for the `Device` model:

    /device/
        /<lookup_url_kwarg>/
            /<action>/

    The device list and detail endpoints are read-only for now, while
    the action endpoint is post-only and delegates to the device's app.
    """
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Only return the devices for a specific User.
        """
        return Device.objects.for_user(self.request.user)

    def get(self, request, *args, **kwargs):
        """
        If the `lookup_url_kwarg` is passed in `kwargs`, then respond
        like a detail view, otherwise respond like a list view.
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Only the command and status endpoints support post for now.
        An additional `action` url kwarg must be specified to know which
        action to perform.

        A 404 is raised if `action` is not specified (indicating a post 
        to the detail or list endpoints) or if it is not in the
        `action_names` attribute.
        """
        instance = self.get_object()
        action = kwargs.get('action', None)
        app = instance.get_app()
        if action is None or action not in app.get_action_names():
            raise Http404
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
        return 'Added {0} device'.format(self.object.name)

    def get_context_data(self, **kwargs):
        """
        Add a `devices` entry with available devices.
        """
        context = super(UserDevicesViewBase, self).get_context_data(**kwargs)
        context['devices'] = Device.objects.for_user(self.request.user).order_by('name')
        return context

    def post(self, request, *args, **kwargs):
        """
        Add the user of this request.
        """
        request.POST = request.POST.copy()
        request.POST['user'] = self.request.user.id
        return super(UserDevicesViewBase, self).post(request, *args, **kwargs)
