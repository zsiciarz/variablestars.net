from django.conf.urls import patterns, url

from .views import StarListView


urlpatterns = patterns('',
    url(r'^$', StarListView.as_view(), name='star_list'),
)
