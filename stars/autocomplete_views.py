from django.db.models.functions import Length

from dal import autocomplete

from .models import Star


class StarAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        stars = Star.objects.all()
        if self.q:
            stars = stars.filter(name__icontains=self.q).order_by(Length('name').asc(), 'name')
        return stars
