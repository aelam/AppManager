__author__ = 'ryan'

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#app_identifier

urlpatterns = patterns('Application.views',
    url(r'^$', 'app_list', name="apps"),
    url(r"^(?P<app_id>\d+)/$", 'app_detail', name="app-detail"),
    url(r'^package/(?P<id>\d+)/$', 'app_packages_list'),
    url(r"^install/", "ota_plist", name="app-install"),
    url(r"^upload/", "package_upload"),
    # url(r"^upload/","pack_upload2"),
    url(r'^package/save/$', 'package_update'),
    # url(r'^package/$','package_list'),
    url(r'^provs/$', 'provisioning_profile_list'),
    # url(r'^package/$','package_list'),
    url(r"^appstore", "appstore"),
)

# urlpatterns += patterns('Application.api',
#     url(r'^api$', 'apps'),
# )
