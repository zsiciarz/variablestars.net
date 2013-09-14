# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from pyaavso.formats.visual import VisualFormatReader

from .models import Observation
from stars.models import Star
from observers.models import Observer


class BatchUploadForm(forms.Form):
    aavso_file = forms.FileField(label=_("Observations file"))

    def process_file(self):
        fp = self.cleaned_data['aavso_file']
        reader = VisualFormatReader(fp)
        observer = Observer.objects.get(aavso_code=reader.observer_code)
        for row in reader:
            try:
                star = Star.objects.get(name=row['name'])
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
            except Exception as e:
                print row
                print e
                continue
