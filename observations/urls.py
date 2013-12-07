from django.conf.urls import patterns, url

from .views import AddObservationView, UploadObservationsView


urlpatterns = patterns('',
    url(r'^add/$', AddObservationView.as_view(), name='add_observation'),
    url(r'^upload/$', UploadObservationsView.as_view(), name='upload_observations'),
)
