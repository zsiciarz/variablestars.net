from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

import ephem
from geoposition.fields import GeopositionField
from model_utils.models import TimeStampedModel

from observations.models import Observation


class ObserverQuerySet(QuerySet):
    def with_observations_count(self):
        return self.annotate(observations_count=Count("observations"))

    def get_total_stats(self):
        today = timezone.now()
        last_month = today - timedelta(days=30)
        last_week = today - timedelta(days=7)
        return {
            "total_observer_count": self.count(),
            "last_month_active_count": self.filter(
                user__last_login__gt=last_month
            ).count(),
            "last_week_active_count": self.filter(
                user__last_login__gt=last_week
            ).count(),
        }


class Observer(TimeStampedModel):
    user = models.OneToOneField(
        "auth.User", editable=False, related_name="observer", on_delete=models.CASCADE,
    )
    aavso_code = models.CharField(
        max_length=10,
        blank=True,
        default="",
        verbose_name=_("AAVSO observer code"),
        help_text=_("This is the code that is officially assigned to you by AAVSO."),
    )
    limiting_magnitude = models.FloatField(
        blank=True,
        null=True,
        default=6.0,
        verbose_name=_("Limiting magnitude of your equipment"),
        help_text=_(
            "The magnitude of the faintest stars you can see with your eyes/binoculars/telescope. Setting this value will affect which stars will have their brightness value(s) grayed out."
        ),
    )
    location = GeopositionField(blank=True)
    city = models.CharField(max_length=255, blank=True, default="",)

    objects = ObserverQuerySet.as_manager()

    class Meta:
        verbose_name = _("Observer")
        verbose_name_plural = _("Observers")
        ordering = ("-created",)

    def __str__(self):
        full_name = self.user.get_full_name()
        if full_name:
            return "%s (%s)" % (self.user, full_name)
        else:
            return str(self.user)

    @models.permalink
    def get_absolute_url(self):
        return ("observers:observer_detail", [], {"pk": self.pk})

    def top_stars(self):
        return Observation.objects.top_stars().filter(observer=self)

    def recent_observations(self):
        return self.observations.select_related("star").order_by("-jd")

    def observed_stars_count(self):
        return self.observations.aggregate(c=Count("star", distinct=True))["c"]

    def get_pyephem_city(self):
        city = ephem.Observer()
        # convert coordinates from degrees to radians
        city.lon = float(self.location.longitude) * ephem.pi / 180.0
        city.lat = float(self.location.latitude) * ephem.pi / 180.0
        return city


def create_observer(sender, instance, created, **kwargs):
    if created:
        Observer.objects.create(user=instance)


post_save.connect(
    create_observer, sender=User, dispatch_uid="observers.models.create_observer"
)
