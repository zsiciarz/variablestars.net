from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'variablestars.views.index', name='main'),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^stars/', include('stars.urls', namespace='stars')),
    url(r'^observers/', include('observers.urls', namespace='observers')),
    url(r'^observations/', include('observations.urls', namespace='observations')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^404/', TemplateView.as_view(template_name='404.html')),
)
