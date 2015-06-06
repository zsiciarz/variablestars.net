from django.utils.translation import ugettext_lazy as _

import autocomplete_light.shortcuts as al

from .models import Star


class StarAutocomplete(al.AutocompleteModelTemplate):
    search_fields = ['name']
    autocomplete_template = "stars/autocomplete.html"
    autocomplete_js_attributes = {
        'placeholder': _("Enter star name"),
    }


al.register(Star, StarAutocomplete)
