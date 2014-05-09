from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from .views import *

# URL Handlers
urlpatterns = patterns(
    '',
    # ADMIN Panel
    url(r'^admin/', include(admin.site.urls)),
    # WEB content
    url(r'^$', pageResults, name='results'),
    #url(r'^login/', pageLogin, name='login'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    url(r'^judge/', pageJudge, name='judge'),
    # REST API
    url(r'^api/', include('RC_Drift_Judgment_backend.api')),
)
