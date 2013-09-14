# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
from registration.signals import user_registered


@python_2_unicode_compatible
class Observer(TimeStampedModel):
    user = models.OneToOneField(
        'auth.User', editable=False, related_name='observer'
    )
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
        full_name = self.user.get_full_name()
        if full_name:
            return '%s (%s)' % (self.user, full_name)
        else:
            return str(self.user)

    @models.permalink
    def get_absolute_url(self):
        return ('observers:observer_detail', [], {'pk': self.pk})


def create_observer(sender, instance, created, **kwargs):
    if created:
        Observer.objects.create(user=instance)


post_save.connect(
    create_observer, sender=User,
    dispatch_uid='observers.models.create_observer'
)


def complete_registration(sender, user, request, **kwargs):
    messages.success(request, _("Thank you for your registration!"))


user_registered.connect(
    complete_registration,
    dispatch_uid='observers.models.complete_registration'
)
