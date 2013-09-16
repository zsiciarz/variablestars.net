from __future__ import unicode_literals

from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

import ephem
from braces.views import SelectRelatedMixin
from pygcvs import dict_to_body

from .models import Star, CONSTELLATIONS_DICT, VariabilityType


class StarListView(SelectRelatedMixin, ListView):
    """
    Display a list of variable stars.
    """
    model = Star
    select_related = ('variability_type',)
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(StarListView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context.update(queryset.get_total_stats(self.request.observer))
        return context


class ConstellationListView(StarListView):
    """
    List all stars in a given constellation.
    """
    allow_empty = False

    def get_queryset(self):
        queryset = super(ConstellationListView, self).get_queryset()
        return queryset.filter(constellation=self.kwargs['constellation'])

    def get_context_data(self, **kwargs):
        context = super(ConstellationListView, self).get_context_data(**kwargs)
        name = CONSTELLATIONS_DICT.get(self.kwargs['constellation'])
        context['constellation'] = name
        return context


class StarSearchView(StarListView):
    """
    Display a list of all stars matching submitted query.
    """
    template_name = "stars/star_search.html"

    def get_queryset(self):
        q = self.request.REQUEST.get('q', '').strip()
        queryset = super(StarSearchView, self).get_queryset()
        self.exact_match = None
        try:
            self.exact_match = queryset.filter(name__iexact=q)[0]
            # doesn't matter what queryset is returned here
            # as we will redirect to exact match anyway
            return queryset
        except IndexError:
            return queryset.filter(name__icontains=q)

    def render_to_response(self, context, **kwargs):
        if self.exact_match:
            return redirect(self.exact_match)
        return super(StarSearchView, self).render_to_response(context, **kwargs)


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
        try:
            next_rising = city.next_rising(body)
        except ephem.CircumpolarError:
            next_rising = None
        context['body'] = body
        context['next_rising'] = next_rising
        observations = star.get_observations_by_observer(self.request.observer)
        context['observations_by_observer'] = observations
        return context


class VariabilityTypeDetailView(DetailView):
    """
    Detailed view about a variability type.
    """
    model = VariabilityType
