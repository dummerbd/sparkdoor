"""
urls.py - `common` app url routes module.
"""
from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',

    # this needs to be last:
    url(r'^$',
        views.HomeView.as_view(),
        name='home'),
)
