from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from InnerAppStore import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from django.contrib import admin

from django.shortcuts import redirect


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', "InnerAppStore.views.main"),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^app/', include('Application.urls')),

)

#if settings.DEBUG:
if False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
