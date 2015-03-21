from django.conf.urls import patterns, url

from .views import ObserverListView, ObserverDetailView, ObserverEditView


urlpatterns = patterns('',
    url(r'^$', ObserverListView.as_view(), name='observer_list'),
    url(r'^(?P<pk>\d+)/$', ObserverDetailView.as_view(), name='observer_detail'),
    url(r'^edit/$', ObserverEditView.as_view(), name='observer_edit'),
)
