from django.conf.urls import patterns, url

from .views import ObserverDetailView


urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', ObserverDetailView.as_view(), name='observer_detail'),
)
