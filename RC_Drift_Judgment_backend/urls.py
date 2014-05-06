from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from rest_framework import viewsets, routers
from rest_framework import serializers
from django.contrib.auth.models import User

from .views import *

# URL Handlers
urlpatterns = patterns('',
    # ADMIN Panel
    url(r'^results', results, name='results'),
    url(r'^admin/', include(admin.site.urls)),
    # WEB content
    url(r'^$', results, name='home' ),
    # REST API
    url(r'^api/', include('RC_Drift_Judgment_backend.api') ),
)
