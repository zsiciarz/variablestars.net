from django.conf.urls import url

from .views import ObservationListView, AddObservationView, UploadObservationsView


app_name = 'observations'
urlpatterns = [
    url(r'^$', ObservationListView.as_view(), name='observation_list'),
    url(r'^(?P<observer_id>\d+)/$', ObservationListView.as_view(), name='observation_list_by_observer'),
    url(r'^add/$', AddObservationView.as_view(), name='add_observation'),
    url(r'^add/(?P<star_id>\d+)/$', AddObservationView.as_view(), name='add_observation_for_star'),
    url(r'^upload/$', UploadObservationsView.as_view(), name='upload_observations'),
]
