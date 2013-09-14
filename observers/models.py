# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class Observer(TimeStampedModel):
    user = models.OneToOneField('auth.User')
    aavso_code = models.CharField(
        max_length=10, blank=True, default='',
        verbose_name=_("AAVSO-assigned observer code")
    )
    limiting_magnitude = models.FloatField(
        blank=True, null=True, default=6.0,
        verbose_name=_("Limiting magnitude of your equipment")
    )
    # TODO: location field

    class Meta:
        verbose_name = _("Observer")
        verbose_name_plural = _("Observers")
        ordering = ('-created',)

    def __str__(self):
        return str(self.user)
