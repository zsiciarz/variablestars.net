from __future__ import unicode_literals

from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from braces.views import LoginRequiredMixin

from .forms import ObserverForm
from .models import Observer


class ObserverListView(ListView):
    """
    Display a list of observers.
    """
    queryset = Observer.objects.with_observations_count()
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(ObserverListView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context.update(queryset.get_total_stats())
        return context


class ObserverDetailView(DetailView):
    """
    Public profile of an observer.
    """
    model = Observer


class ObserverEditView(LoginRequiredMixin, UpdateView):
    """
    Edit current user's observer profile.
    """
    model = Observer
    form_class = ObserverForm
    template_name_suffix = '_edit'

    def get_object(self):
        return Observer.objects.get(user=self.request.user)
