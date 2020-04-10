from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _


class ObservationManager(models.Manager):
    def top_stars(self):
        queryset = self.values("star_id", "star__name")
        queryset = queryset.annotate(observations_count=Count("star"))
        return queryset.order_by("-observations_count")

    def top_observers(self):
        queryset = self.values(
            "observer_id", "observer__user__username", "observer__aavso_code"
        )
        queryset = queryset.annotate(observations_count=Count("observer"))
        return queryset.order_by("-observations_count")

    def recent_observations(self):
        return self.select_related("star", "observer").order_by("-jd")


class Observation(models.Model):
    """
    Single observation - estimation of variable star's brightness.
    """

    observer = models.ForeignKey(
        "observers.Observer",
        related_name="observations",
        verbose_name=_("Observer"),
        on_delete=models.CASCADE,
    )
    star = models.ForeignKey(
        "stars.Star",
        related_name="observations",
        verbose_name=_("Star"),
        on_delete=models.CASCADE,
    )
    jd = models.FloatField(verbose_name=_("Julian Date"))
    magnitude = models.FloatField(verbose_name=_("Brightness"))
    fainter_than = models.BooleanField(
        default=False, verbose_name=_("Fainter than given magnitude")
    )
    comp1 = models.CharField(
        max_length=5, blank=True, default="", verbose_name=_("First comparison star"),
    )
    comp2 = models.CharField(
        max_length=5, blank=True, default="", verbose_name=_("Second comparison star"),
    )
    comment_code = models.CharField(
        max_length=10, blank=True, default="", verbose_name=_("Comment code")
    )
    chart = models.CharField(
        max_length=20, blank=True, default="", verbose_name=_("Chart")
    )
    notes = models.CharField(
        max_length=100, blank=True, default="", verbose_name=_("Additional notes")
    )

    objects = ObservationManager()

    class Meta:
        verbose_name = _("Observation")
        verbose_name_plural = _("Observations")
        ordering = ["-jd"]

    def __str__(self):
        return "%s %s %s" % (self.star, self.jd, self.magnitude)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.star.observations_count += 1
            self.star.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.star.observations_count -= 1
        self.star.save()
        super().delete(*args, **kwargs)
