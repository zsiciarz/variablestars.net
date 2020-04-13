from django.db import models
from django.db.models import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from observations.models import Observation
from observations.utils import jd_now


CONSTELLATIONS = Choices(
    ("AND", _("Andromeda")),
    ("ANT", _("Antlia")),
    ("APS", _("Apus")),
    ("AQR", _("Aquarius")),
    ("AQL", _("Aquila")),
    ("ARA", _("Ara")),
    ("ARI", _("Aries")),
    ("AUR", _("Auriga")),
    ("BOO", _("Boötes")),
    ("CAE", _("Caelum")),
    ("CAM", _("Camelopardalis")),
    ("CNC", _("Cancer")),
    ("CVN", _("Canes Venatici")),
    ("CMA", _("Canis Major")),
    ("CMI", _("Canis Minor")),
    ("CAP", _("Capricornus")),
    ("CAR", _("Carina")),
    ("CAS", _("Cassiopeia")),
    ("CEN", _("Centaurus")),
    ("CEP", _("Cepheus")),
    ("CET", _("Cetus")),
    ("CHA", _("Chamaeleon")),
    ("CIR", _("Circinus")),
    ("COL", _("Columba")),
    ("COM", _("Coma Berenices")),
    ("CRA", _("Corona Australis")),
    ("CRB", _("Corona Borealis")),
    ("CRV", _("Corvus")),
    ("CRT", _("Crater")),
    ("CRU", _("Crux")),
    ("CYG", _("Cygnus")),
    ("DEL", _("Delphinus")),
    ("DOR", _("Dorado")),
    ("DRA", _("Draco")),
    ("EQU", _("Equuleus")),
    ("ERI", _("Eridanus")),
    ("FOR", _("Fornax")),
    ("GEM", _("Gemini")),
    ("GRU", _("Grus")),
    ("HER", _("Hercules")),
    ("HOR", _("Horologium")),
    ("HYA", _("Hydra")),
    ("HYI", _("Hydrus")),
    ("IND", _("Indus")),
    ("LAC", _("Lacerta")),
    ("LEO", _("Leo")),
    ("LMI", _("Leo Minor")),
    ("LEP", _("Lepus")),
    ("LIB", _("Libra")),
    ("LUP", _("Lupus")),
    ("LYN", _("Lynx")),
    ("LYR", _("Lyra")),
    ("MEN", _("Mensa")),
    ("MIC", _("Microscopium")),
    ("MON", _("Monoceros")),
    ("MUS", _("Musca")),
    ("NOR", _("Norma")),
    ("OCT", _("Octans")),
    ("OPH", _("Ophiuchus")),
    ("ORI", _("Orion")),
    ("PAV", _("Pavo")),
    ("PEG", _("Pegasus")),
    ("PER", _("Perseus")),
    ("PHE", _("Phoenix")),
    ("PIC", _("Pictor")),
    ("PSC", _("Pisces")),
    ("PSA", _("Piscis Austrinus")),
    ("PUP", _("Puppis")),
    ("PYX", _("Pyxis")),
    ("RET", _("Reticulum")),
    ("SGE", _("Sagitta")),
    ("SGR", _("Sagittarius")),
    ("SCO", _("Scorpius")),
    ("SCL", _("Sculptor")),
    ("SCT", _("Scutum")),
    ("SER", _("Serpens")),
    ("SEX", _("Sextans")),
    ("TAU", _("Taurus")),
    ("TEL", _("Telescopium")),
    ("TRI", _("Triangulum")),
    ("TRA", _("Triangulum Australe")),
    ("TUC", _("Tucana")),
    ("UMA", _("Ursa Major")),
    ("UMI", _("Ursa Minor")),
    ("VEL", _("Vela")),
    ("VIR", _("Virgo")),
    ("VOL", _("Volans")),
    ("VUL", _("Vulpecula")),
)

CONSTELLATIONS_DICT = dict(CONSTELLATIONS)


class StarQuerySet(QuerySet):
    def get_total_stats(self, observer=None):
        last_month = jd_now() - 30
        star_ids = Observation.objects.filter(jd__gt=last_month).values("star")
        if observer:
            observed_ids = observer.observations.values("star")
        else:
            observed_ids = []
        return {
            "total_star_count": self.count(),
            "observed_last_month_count": self.filter(pk__in=star_ids).count(),
            "observed_by_you_count": self.filter(pk__in=observed_ids).count(),
        }


class Star(models.Model):
    """
    A variable star.
    """

    constellation = models.CharField(
        _("Constellation"), max_length=3, choices=CONSTELLATIONS, db_index=True
    )
    name = models.CharField(_("Name"), max_length=20, db_index=True)
    ra = models.CharField(_("Right Ascension"), max_length=15, default="")
    dec = models.CharField(_("Declination"), max_length=15, default="")
    variability_type = models.ForeignKey(
        "stars.VariabilityType",
        null=True,
        blank=True,
        verbose_name=_("Type of variability"),
        on_delete=models.CASCADE,
    )
    max_magnitude = models.FloatField(_("Maximum brightness"), null=True)
    min_magnitude = models.FloatField(_("Minimum brightness"), null=True)
    epoch = models.FloatField(_("Epoch"), null=True)
    period = models.FloatField(_("Period"), null=True)

    # denormalization
    observations_count = models.PositiveIntegerField(default=0, editable=False)

    objects = StarQuerySet.as_manager()

    class Meta:
        verbose_name = _("Variable star")
        verbose_name_plural = _("Variable stars")
        ordering = ("constellation", "name")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("stars:star_detail", kwargs={"pk": self.pk})

    def is_periodic(self):
        """
        Returns True if the star is periodic (has a defined period and epoch).
        """
        return self.epoch is not None and self.period is not None

    def get_gcvs_search_name(self):
        """
        Fixes GCVS inconsequence in handling escape characters.
        """
        return self.name.replace(" ", "+")

    def top_observers(self):
        return Observation.objects.top_observers().filter(star=self)

    def observers_count(self):
        return self.observations.aggregate(c=Count("observer", distinct=True))["c"]

    def recent_observations(self):
        return self.observations.select_related("observer").order_by("-jd")

    def get_observations_by_observer(self, observer):
        return self.observations.filter(observer=observer)


class VariabilityType(models.Model):
    """
    A short description of variability type from GCVS.
    """

    code = models.CharField(_("Letter code"), max_length=12, db_index=True)
    short_description = models.CharField(
        _("Short description"), max_length=100, blank=True, default=""
    )
    long_description = models.TextField(_("Long description"), default="")

    class Meta:
        verbose_name = _("Variability type")
        verbose_name_plural = _("Variability types")
        ordering = ("code",)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("stars:variabilitytype_detail", kwargs={"pk": self.pk})
