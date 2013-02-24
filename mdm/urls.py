# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('mdm.views',
    url(r'^/?$', 'main', name='mdm-main'),
    url(r'^checkin/?$', 'checkin', name='mdm-checkin'),
)
