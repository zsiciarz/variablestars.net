# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Observer


def get_current_observer(request):
    if request.user and request.user.is_authenticated:
        current_observer = Observer.objects.get(user=request.user)
    else:
        current_observer = None
    return {
        'current_observer': current_observer,
    }
