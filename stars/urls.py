from django.conf.urls import patterns, url

from .views import StarListView, ConstellationListView, StarSearchView, \
    StarDetailView, VariabilityTypeDetailView


urlpatterns = patterns('',
    url(r'^$', StarListView.as_view(), name='star_list'),
    url(r'^(?P<pk>\d+)/$', StarDetailView.as_view(), name='star_detail'),
    url(r'^(?P<constellation>[A-Z]{3})/$', ConstellationListView.as_view(), name='constellation_list'),
    url(r'^search/$', StarSearchView.as_view(), name='star_search'),
    url(r'^type/(?P<code>[/\(\)\+\*\:\w]+)/$', VariabilityTypeDetailView.as_view(), name='variabilitytype_detail'),
)
