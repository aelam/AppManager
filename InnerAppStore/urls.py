from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from InnerAppStore import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
#
urlpatterns = patterns('',
    # url(
    #    r'^accounts/login/$','django.contrib.auth.views.login',
    #    dict(
    #        template_name = 'jqm/login.html',
    #        ),
    #    name='login',
    #    ),
    # url(
    #    r'^accounts/logout/$','django.contrib.auth.views.logout',
    #    dict(
    #        template_name = 'jqm/logout.html',
    #        ),
    #    name='logout',
    #    ),

    # url(r'^(?P<url>.*)$', 'django.contrib.flatpages.sights.flatpage', title='flatpage'),
    url(r'^$', "InnerAppStore.views.main", name="main"),
    #url(r'^$', "InnerAppStore.views.main", name="main"),
    # url(r"^$", 'django.views.generic.simple.redirect_to', {'url': 'app'}, name="main"),
    url(r'^app/', include('Application.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mdm/', include("mdm.urls"), name='mdm'),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    # url(r'^api/', include('Application.api_urls')),

    url(r'^mdm/', include("mdm.urls")),
    (r'^scep/', include('scep.urls')),

    # url(r'^accounts/', include('django.contrib.auth.urls')),
    # url(r'^accounts/', include('registration.backends.default.urls')),
    (r'^accounts/', include('userena.urls')),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()


