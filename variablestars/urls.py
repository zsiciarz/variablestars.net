from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'variablestars.views.index', name='main'),
    url(r'^stars/', include('stars.urls', namespace='stars')),
    url(r'^admin/', include(admin.site.urls)),
)
