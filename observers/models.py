# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from django.db.models import Count
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel
from registration.signals import user_registered


class ObserverQuerySet(QuerySet):
    def with_observations_count(self):
        return self.annotate(observations_count=Count('observations'))

    def get_total_stats(self):
        last_month = date.today() - timedelta(days=30)
        last_week = date.today() - timedelta(days=7)
        return {
            'total_observer_count': self.count(),
            'last_month_active_count': self.filter(user__last_login__gt=last_month).count(),
            'last_week_active_count': self.filter(user__last_login__gt=last_week).count(),
        }


@python_2_unicode_compatible
class Observer(TimeStampedModel):
    user = models.OneToOneField(
        'auth.User', editable=False, related_name='observer'
    )
    aavso_code = models.CharField(
        max_length=10, blank=True, default='',
        verbose_name=_("AAVSO observer code"),
        help_text=_("This is the code that is officially assigned to you by AAVSO.")
    )
    limiting_magnitude = models.FloatField(
        blank=True, null=True, default=6.0,
        verbose_name=_("Limiting magnitude of your equipment"),
        help_text=_("The magnitude of the faintest stars you can see with your eyes/binoculars/telescope. Setting this value will affect which stars will have their brightness value(s) grayed out.")
    )
    # TODO: location field

    objects = PassThroughManager.for_queryset_class(ObserverQuerySet)()

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

    def top_stars(self):
        queryset = self.observations.values('star_id', 'star__name')
        queryset = queryset.annotate(observations_count=Count('star'))
        return queryset.order_by('-observations_count')

    def recent_observations(self):
        return self.observations.select_related('star').order_by('-jd')

    def observed_stars_count(self):
        return self.observations.aggregate(c=Count('star', distinct=True))['c']


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
