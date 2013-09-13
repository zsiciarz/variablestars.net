from __future__ import unicode_literals

from django.http import Http404
from django.views.generic import ListView, DetailView

from .models import Star, CONSTELLATIONS_DICT


class StarListView(ListView):
    """
    Display a list of variable stars.
    """
    model = Star
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(StarListView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['total_star_count'] = queryset.count()
        return context


class ConstellationListView(StarListView):
    """
    List all stars in a given constellation.
    """
    allow_empty = False

    def get_queryset(self):
        return Star.objects.filter(constellation=self.kwargs['constellation'])

    def get_context_data(self, **kwargs):
        context = super(ConstellationListView, self).get_context_data(**kwargs)
        name = CONSTELLATIONS_DICT.get(self.kwargs['constellation'])
        context['constellation'] = name
        return context


class StarSearchView(ListView):
    """
    Display a list of all stars matching submitted query.
    """
    model = Star
    paginate_by = 20
    template_name = "stars/star_search.html"

    def get_queryset(self):
        q = self.request.REQUEST.get('q')
        return Star.objects.filter(name__icontains=q)


class StarDetailView(DetailView):
    """
    Detailed information about a variable star.
    """
    model = Star
