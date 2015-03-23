from django.utils.translation import ugettext_lazy as _

import autocomplete_light

from .models import Star


class StarAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    search_fields = ['name']
    autocomplete_template = "stars/autocomplete.html"
    autocomplete_js_attributes = {
        'placeholder': _("Enter star name"),
    }


autocomplete_light.register(Star, StarAutocomplete)
