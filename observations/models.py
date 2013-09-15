# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Observation(models.Model):
    """
    Single observation - estimation of variable star's brightness.
    """
    observer = models.ForeignKey(
        'observers.Observer', related_name='observations',
        verbose_name=_("Observer")
    )
    star = models.ForeignKey(
        'stars.Star', related_name='observations', verbose_name=_("Star")
    )
    jd = models.FloatField(verbose_name=_("Julian Date"))
    magnitude = models.FloatField(verbose_name=_("Brightness"))
    fainter_than = models.BooleanField(
        default=False, verbose_name=_("Fainter than given magnitude")
    )
    comp1 = models.CharField(
        max_length=5, blank=True, default='',
        verbose_name=_("First comparison star"),
    )
    comp2 = models.CharField(
        max_length=5, blank=True, default='',
        verbose_name=_("Second comparison star"),
    )
    comment_code = models.CharField(
        max_length=10, blank=True, default='', verbose_name=_("Comment code")
    )
    chart = models.CharField(
        max_length=20, blank=True, default='', verbose_name=_("Chart")
    )
    notes = models.CharField(
        max_length=100, blank=True, default='',
        verbose_name=_("Additional notes")
    )

    class Meta:
        verbose_name = _("Observation")
        verbose_name_plural = _("Observations")

    def __str__(self):
        return "%s %s %s" % (self.star, self.jd, self.magnitude)
