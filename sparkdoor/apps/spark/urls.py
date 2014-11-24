"""
urls.py - `spark` app url routes module.
"""
from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',

    url(r'^devices/$',
        views.DeviceAPIView.as_view(),
        name='devices-list'
    ),
    
    url(r'^devices/(?P<pk>\d+)/$',
        views.DeviceAPIView.as_view(),
        name='devices-detail'
    ),

    url(r'^devices/(?P<pk>\d+)/(?P<action>[\w\d-]+)/$',
        views.DeviceAPIView.as_view(),
        name='devices-action'
    )
)
