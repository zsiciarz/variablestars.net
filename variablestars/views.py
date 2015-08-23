from django.shortcuts import render

from stars.models import Star
from observations.models import Observation
from observers.models import Observer


def index(request):
    return render(request, "index.html", {
        'stars_count': Star.objects.count(),
        'observers_count': Observer.objects.count(),
        'observations_count': Observation.objects.count(),
        'top_stars': Observation.objects.top_stars(),
        'recent_observations': Observation.objects.recent_observations(),
    })
