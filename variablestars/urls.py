from django.conf.urls import include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from .views import index

urlpatterns = [
    url(r'^$', index, name='main'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^stars/', include('stars.urls', namespace='stars')),
    url(r'^observers/', include('observers.urls', namespace='observers')),
    url(r'^observations/', include('observations.urls', namespace='observations')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^404/', TemplateView.as_view(template_name='404.html')),
]
