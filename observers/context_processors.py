# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def get_current_observer(request):
    return {
        'current_observer': getattr(request, 'observer', None),
    }
