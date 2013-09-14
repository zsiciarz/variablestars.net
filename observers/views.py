from __future__ import unicode_literals

from django.views.generic import ListView, DetailView

from .models import Observer


class ObserverDetailView(DetailView):
    """
    Public profile of an observer.
    """
    model = Observer
