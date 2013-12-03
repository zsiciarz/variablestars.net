# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from pyaavso.formats.visual import VisualFormatReader

from .models import Observation
from stars.models import Star
from observers.models import Observer


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
                    self.process_row(row, observer)
                except Exception as e:
                    print row
                    print e
                    continue

    def process_row(self, row, observer):
        name = self.normalize_star_name(row['name'])
        star = Star.objects.get(name=name)
        fainter_than = '<' in row['magnitude']
        magnitude = float(row['magnitude'].replace('<', ''))
        jd = float(row['date'])
        try:
            observation = Observation.objects.get(
                observer=observer,
                star=star,
                jd=jd,
            )
        except Observation.DoesNotExist:
            observation = Observation(
                observer=observer,
                star=star,
                jd=jd,
            )
        observation.magnitude = magnitude
        observation.fainter_than = fainter_than
        observation.comp1 = row['comp1']
        observation.comp2 = row['comp2']
        observation.chart = row['chart']
        observation.comment_code = row['comment_code']
        observation.notes = row['notes']
        observation.save()

    def normalize_star_name(self, name):
        """
        Normalize star name with GCVS names, for example: V339 -> V0339.
        """
        digits = '123456789'
        if name[0] == 'V' and name[1] in digits and name[4] not in digits:
            name = 'V0' + name[1:]
        return name
