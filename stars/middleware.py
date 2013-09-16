# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class StarFilterMiddleware(object):
    """
    Stores star filter data in user's session.
    """
    def process_request(self, request):
        assert hasattr(request, 'session'), "StarFilterMiddleware requires session middleware to be installed."
        limiting_magnitude = request.GET.get('limiting_magnitude')
        if limiting_magnitude:
            if limiting_magnitude == 'None':
                limiting_magnitude = None
            request.session['limiting_magnitude'] = limiting_magnitude