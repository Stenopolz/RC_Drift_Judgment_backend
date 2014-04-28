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
    url(r'^admin/', include(admin.site.urls)),
    # WEB content
    url(r'^$', home, name='home' ),
    # REST API
    ## judges
    url(r'^api/judges/$', JudgeList.as_view(), name='judge-list'),
    url(r'^api/judges/(?P<pk>\d+)/$', JudgeDetail.as_view(), name='judge-detail'),
    ## pilots
    url(r'^api/pilots/$', PilotList.as_view(), name='pilot-list'),
    url(r'^api/pilots/(?P<pk>\d+)/$', PilotDetail, name='pilot-detail'),
    ## marks
    url(r'^api/marks/$', RaceMarkList.as_view(), name='mark-list'),
    url(r'^api/marks/(?P<pk>\d+)/$', RaceMarkDetail.as_view(), name='mark-detail'),
    # misk
    url(r'^api/', api_root, name='api-root'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
