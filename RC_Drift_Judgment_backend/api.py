from django.conf.urls import patterns, include, url

from .views_api import *

# URL Handlers
urlpatterns = patterns('',
    # REST API
    ## judges
    url(r'^judges/$', JudgeList.as_view(), name='judge-list'),
    url(r'^judges/(?P<pk>\d+)/$', JudgeDetail.as_view(), name='judge-detail'),
    ## pilots
    url(r'^pilots/$', PilotList.as_view(), name='pilot-list'),
    url(r'^pilots/(?P<pk>\d+)/$', PilotDetail, name='pilot-detail'),
    ## marks
    url(r'^marks/$', RaceMarkList.as_view(), name='mark-list'),
    url(r'^marks/(?P<pk>\d+)/$', RaceMarkDetail.as_view(), name='mark-detail'),
    ## RaceResults
    url(r'^results/$', RaceResults, name='results-detail'),
    # API Root
    url(r'^', api_root, name='api-root'),
    # API Auth
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
)
