from __future__ import unicode_literals

from django.views.generic import ListView, DetailView

from .models import Observer


class ObserverListView(ListView):
    """
    Display a list of observers.
    """
    model = Observer
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(ObserverListView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['total_observer_count'] = queryset.count()
        return context


class ObserverDetailView(DetailView):
    """
    Public profile of an observer.
    """
    model = Observer
