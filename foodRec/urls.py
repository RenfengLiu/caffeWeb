from django.conf.urls import patterns, include, url
from django.contrib import admin

from AppServer import views, urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('AppServer.urls')),
    url(r'^(.*)',include('AppServer.urls'))
)
