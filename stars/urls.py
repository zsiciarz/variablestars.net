from django.conf.urls import url

from .views import StarListView, StarsInConstellationListView, StarSearchView, \
    StarDetailView, VariabilityTypeListView, VariabilityTypeDetailView, \
    ConstellationListView, recent_observations


urlpatterns = [
    url(r'^$', StarListView.as_view(), name='star_list'),
    url(r'^variability_types/$', VariabilityTypeListView.as_view(), name='variabilitytype_list'),
    url(r'^constellations/$', ConstellationListView.as_view(), name='constellation_list'),
    url(r'^(?P<pk>\d+)/$', StarDetailView.as_view(), name='star_detail'),
    url(r'^(?P<constellation>[A-Z]{3})/$', StarsInConstellationListView.as_view(), name='constellation_list'),
    url(r'^search/$', StarSearchView.as_view(), name='star_search'),
    url(r'^type/(?P<pk>\d+)/$', VariabilityTypeDetailView.as_view(), name='variabilitytype_detail'),

    url(r'^(?P<pk>\d+)\.csv$', recent_observations, name='recent_observations'),
]
