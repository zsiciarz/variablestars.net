from django import forms
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

import autocomplete_light.shortcuts as al
from pyaavso.formats.visual import VisualFormatReader

from .models import Observation
from .utils import dict_to_observation
from observers.models import Observer


class ObservationForm(al.ModelForm):
    class Meta:
        model = Observation
        fields = (
            'star', 'jd', 'magnitude', 'fainter_than', 'comp1', 'comp2',
            'comment_code', 'chart', 'notes',
        )
        autocomplete_fields = ('star',)


class BatchUploadForm(forms.Form):
    aavso_file = forms.FileField(
        label=_("Observations file"),
        help_text=_("Upload a file in <a href=\"http://www.aavso.org/aavso-visual-file-format\">AAVSO Visual File Format.")
    )

    def process_file(self):
        fp = self.cleaned_data['aavso_file']
        # force the input to be a real Python generator
        reader = VisualFormatReader(line for line in fp)
        observer = Observer.objects.get(aavso_code=reader.observer_code)
        with transaction.atomic():
            for row in reader:
                try:
                    observation = dict_to_observation(row, observer)
                    observation.save()
                except Exception:
                    continue
