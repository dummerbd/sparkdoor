"""
views.py - `common` app views module.
"""
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView

from rest_framework import views, response, serializers

from sparkdoor.apps.spark.views import UserDevicesViewBase

from .models import IDCard


class HomeView(TemplateView):
    """
    The home page view.
    """
    template_name = 'common/home.html'


class ProfileView(UserDevicesViewBase):
    """
    The user profile view, which provides a list of the user's devices
    and a device registration form.
    """
    template_name = 'common/devices.html'
    success_url = reverse_lazy('common:profile')


class IDCardOpenSerializer(serializers.Serializer):
    """
    Serializer for the `IDCardOpenView`.
    """
    device_id = serializers.CharField(max_length=250)
    card_uid = serializers.CharField(max_length=200)


class IDCardOpenView(views.APIView):
    """
    API view that is POSTed to by a door device. The POST data must
    include a `device_id` and a `card_uid`. If a match is successfull,
    indicating that the door can be opened, a 200 is returned, otherwise
    a 403. 
    """
    def post(self, request, *args, **kwargs):
        """
        POST handler.
        """
        serializer = IDCardOpenSerializer(data=request.DATA)
        if not serializer.is_valid():
            print(serializer.errors)
            return response.Response('Invalid request data.', 400)
        if self.can_open_door(serializer.data):
            return response.Response('Valid ID card.', 200)
        return response.Response('Invalid ID card.', 403)

    def can_open_door(self, data):
        """
        Check if the provided `card_uid` is allowed to open the door
        that corresponds to the provided `device_id`.
        """
        try:
            card = IDCard.objects.get(device__device_id=data['device_id'],
                uid=data['card_uid'])
        except:
            return False
        return True
