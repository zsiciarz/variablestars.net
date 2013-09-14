from django.conf.urls import patterns, url

from .views import UploadObservationsView


urlpatterns = patterns('',
    url(r'^upload/$', UploadObservationsView.as_view(), name='upload_observations'),
)
