from __future__ import unicode_literals

from django.forms.models import model_to_dict
from django.http import Http404
from django.views.generic import ListView, DetailView

import ephem
from pygcvs import dict_to_body

from .models import Star, CONSTELLATIONS_DICT, VariabilityType


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

    def get_context_data(self, **kwargs):
        context = super(StarDetailView, self).get_context_data(**kwargs)
        star = context['star']
        body = dict_to_body(model_to_dict(star))
        # TODO: consider observer's location
        city = ephem.city('Warsaw')
        body.compute(city)
        context['body'] = body
        return context


class VariabilityTypeDetailView(DetailView):
    """
    Detailed view about a variability type.
    """
    model = VariabilityType
    slug_field = slug_url_kwarg = 'code'
