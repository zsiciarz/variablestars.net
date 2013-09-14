from django.conf.urls import patterns, url

from .views import ObserverListView, ObserverDetailView, ObserverEditView


urlpatterns = patterns('',
    url(r'^$', ObserverListView.as_view(), name='observer_list'),
    url(r'^(?P<pk>\d+)/$', ObserverDetailView.as_view(), name='observer_detail'),
    url(r'^edit/$', ObserverEditView.as_view(), name='observer_edit'),
    url(r'^change_password/$', 'django.contrib.auth.views.password_change', name='change_password', kwargs={'post_change_redirect': '/'}),
    url(r'^reset_password/$', 'django.contrib.auth.views.password_reset', name='reset_password', kwargs={'post_reset_redirect': 'auth_password_reset_done'}),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='reset_password_confirm', kwargs={'post_reset_redirect': 'auth_password_reset_complete'}),
)
