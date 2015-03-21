from __future__ import unicode_literals

import csv
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView

import ephem
from braces.views import SelectRelatedMixin
from pygcvs import dict_to_body

from .models import Star, CONSTELLATIONS_DICT, VariabilityType
from observations.utils import jd_now


class StarListView(SelectRelatedMixin, ListView):
    """
    Display a list of variable stars.
    """
    model = Star
    select_related = ('variability_type',)

    def get_queryset(self):
        queryset = super(StarListView, self).get_queryset()
        try:
            magnitude = float(self.request.session['limiting_magnitude'])
            queryset = queryset.filter(max_magnitude__lt=magnitude)
        except Exception:
            pass
        try:
            stars_with_observations = self.request.session['stars_with_observations']
            if stars_with_observations:
                queryset = queryset.filter(observations_count__gt=0)
        except Exception:
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StarListView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context.update(queryset.get_total_stats(self.request.observer))
        return context


class ConstellationListView(StarListView):
    """
    List all stars in a given constellation.
    """
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
        observer = self.request.observer
        if observer:
            city = observer.get_pyephem_city()
        else:
            city = ephem.city('Warsaw')
        body.compute(city)
        context['star_altitude'] = body.alt
        context['star_azimuth'] = body.az
        try:
            next_rising = city.next_rising(body)
        except ephem.CircumpolarError:
            next_rising = None
        context['body'] = body
        context['next_rising'] = next_rising
        observations = star.get_observations_by_observer(observer)
        context['observations_by_observer'] = observations
        return context


class VariabilityTypeDetailView(StarListView):
    """
    Detailed view about a variability type.
    """
    template_name = "stars/variabilitytype_detail.html"

    def get_queryset(self):
        queryset = super(VariabilityTypeDetailView, self).get_queryset()
        return queryset.filter(variability_type_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(VariabilityTypeDetailView, self).get_context_data(**kwargs)
        context['variabilitytype'] = VariabilityType.objects.get(pk=self.kwargs['pk'])
        return context


def recent_observations(request, pk):
    """
    Poor man's CSV data dump of recent observations of given star.

    TODO: separate the code elsewhere (or use some API framework)
    """
    star = get_object_or_404(Star, pk=pk)
    min_jd = jd_now() - 5000.0  # TODO: would be nice to customize this
    observations = star.observations.filter(jd__gt=min_jd)
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['jd', 'magnitude'])
    for observation in observations:
        writer.writerow([observation.jd, observation.magnitude])
    return response
