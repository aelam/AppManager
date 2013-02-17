__author__ = 'ryan'

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#app_identifier

urlpatterns = patterns('Application.views',
    url(r'^$','app_list'),
    url(r"^(?P<app_id>\d+)/$",'app_detail'),
    url(r'^package/(?P<id>\d+)/$','app_packages_list'),
    url(r"^install/","ota_plist"),
    url(r"^upload/","package_upload"),
    # url(r"^upload/","pack_upload2"),
    url(r'^package/save/$','package_update'),
    # url(r'^package/$','package_list'),

)
