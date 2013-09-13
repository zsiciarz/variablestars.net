from django.conf.urls import patterns, url

from .views import StarListView, StarSearchView, StarDetailView


urlpatterns = patterns('',
    url(r'^$', StarListView.as_view(), name='star_list'),
    url(r'^(?P<pk>\d+)/$', StarDetailView.as_view(), name='star_detail'),
    url(r'^search/$', StarSearchView.as_view(), name='star_search'),
)
