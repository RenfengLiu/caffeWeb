from django.conf.urls import patterns, include, url
from django.contrib import admin

from AppServer import views, urls

urlpatterns = patterns('',
    url(r'^$',views.fileupload_view ,name='fileupload_view'),
    url(r'^fileupload/$', views.fileupload_view ,name='fileupload_view'),
    url(r'^classifyimage', views.classifyimage_view, name='classifyimage_view')
)
