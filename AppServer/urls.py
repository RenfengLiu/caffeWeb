from django.conf.urls import patterns, url

import views

# from AppServer import debug_view

urlpatterns = patterns('',
    url(r'^$',views.fileupload_view ,name='fileupload_view'),
    url(r'^/fileupload$', views.fileupload_view ,name='fileupload_view')
    # 
    # URL for debug 
    # url(r'^photos/$',debug_view.photo_list_vew,name='photos'),
    # url(r'^photos/(?P<page>\d+)$',debug_view.photo_list_vew,name='photos'),

)
