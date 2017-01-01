from django.conf.urls import url

from .views import ObserverListView, ObserverDetailView, ObserverEditView


app_name = 'observers'
urlpatterns = [
    url(r'^$', ObserverListView.as_view(), name='observer_list'),
    url(r'^(?P<pk>\d+)/$', ObserverDetailView.as_view(), name='observer_detail'),
    url(r'^edit/$', ObserverEditView.as_view(), name='observer_edit'),
]
