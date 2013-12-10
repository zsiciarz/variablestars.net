# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

import autocomplete_light

from .models import Star


class StarAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['name']
    autocomplete_js_attributes = {
        'placeholder': _("Enter star name"),
    }


autocomplete_light.register(Star, StarAutocomplete)
