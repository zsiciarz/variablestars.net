# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect

from stars.models import Star
from observations.models import Observation
from observers.models import Observer


def index(request):
    if request.user.is_authenticated():
        return redirect(request.user)
    return render(request, "index.html", {
        'stars_count': Star.objects.count(),
        'observers_count': Observer.objects.count(),
        'observations_count': Observation.objects.count(),
        'top_stars': Observation.objects.top_stars(),
    })
