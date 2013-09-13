from __future__ import unicode_literals

from django.views.generic import ListView

from .models import Star


class StarListView(ListView):
    """
    Display a list of variable stars.
    """
    model = Star
