from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'variablestars.views.index', name='main'),
    url(r'', include('django.contrib.auth.urls')),
    url(r'^stars/', include('stars.urls', namespace='stars')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^404/', TemplateView.as_view(template_name='404.html')),
)
