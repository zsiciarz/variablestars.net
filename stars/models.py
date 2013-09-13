# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


CONSTELLATIONS = Choices(
    ('AND', _('Andromeda')),
    ('ANT', _('Antlia')),
    ('APS', _('Apus')),
    ('AQR', _('Aquarius')),
    ('AQL', _('Aquila')),
    ('ARA', _('Ara')),
    ('ARI', _('Aries')),
    ('AUR', _('Auriga')),
    ('BOO', _('Boötes')),
    ('CAE', _('Caelum')),
    ('CAM', _('Camelopardalis')),
    ('CNC', _('Cancer')),
    ('CVN', _('Canes Venatici')),
    ('CMA', _('Canis Major')),
    ('CMI', _('Canis Minor')),
    ('CAP', _('Capricornus')),
    ('CAR', _('Carina')),
    ('CAS', _('Cassiopeia')),
    ('CEN', _('Centaurus')),
    ('CEP', _('Cepheus')),
    ('CET', _('Cetus')),
    ('CHA', _('Chamaeleon')),
    ('CIR', _('Circinus')),
    ('COL', _('Columba')),
    ('COM', _('Coma Berenices')),
    ('CRA', _('Corona Australis')),
    ('CRB', _('Corona Borealis')),
    ('CRV', _('Corvus')),
    ('CRT', _('Crater')),
    ('CRU', _('Crux')),
    ('CYG', _('Cygnus')),
    ('DEL', _('Delphinus')),
    ('DOR', _('Dorado')),
    ('DRA', _('Draco')),
    ('EQU', _('Equuleus')),
    ('ERI', _('Eridanus')),
    ('FOR', _('Fornax')),
    ('GEM', _('Gemini')),
    ('GRU', _('Grus')),
    ('HER', _('Hercules')),
    ('HOR', _('Horologium')),
    ('HYA', _('Hydra')),
    ('HYI', _('Hydrus')),
    ('IND', _('Indus')),
    ('LAC', _('Lacerta')),
    ('LEO', _('Leo')),
    ('LMI', _('Leo Minor')),
    ('LEP', _('Lepus')),
    ('LIB', _('Libra')),
    ('LUP', _('Lupus')),
    ('LYN', _('Lynx')),
    ('LYR', _('Lyra')),
    ('MEN', _('Mensa')),
    ('MIC', _('Microscopium')),
    ('MON', _('Monoceros')),
    ('MUS', _('Musca')),
    ('NOR', _('Norma')),
    ('OCT', _('Octans')),
    ('OPH', _('Ophiuchus')),
    ('ORI', _('Orion')),
    ('PAV', _('Pavo')),
    ('PEG', _('Pegasus')),
    ('PER', _('Perseus')),
    ('PHE', _('Phoenix')),
    ('PIC', _('Pictor')),
    ('PSC', _('Pisces')),
    ('PSA', _('Piscis Austrinus')),
    ('PUP', _('Puppis')),
    ('PYX', _('Pyxis')),
    ('RET', _('Reticulum')),
    ('SGE', _('Sagitta')),
    ('SGR', _('Sagittarius')),
    ('SCO', _('Scorpius')),
    ('SCL', _('Sculptor')),
    ('SCT', _('Scutum')),
    ('SER', _('Serpens')),
    ('SEX', _('Sextans')),
    ('TAU', _('Taurus')),
    ('TEL', _('Telescopium')),
    ('TRI', _('Triangulum')),
    ('TRA', _('Triangulum Australe')),
    ('TUC', _('Tucana')),
    ('UMA', _('Ursa Major')),
    ('UMI', _('Ursa Minor')),
    ('VEL', _('Vela')),
    ('VIR', _('Virgo')),
    ('VOL', _('Volans')),
    ('VUL', _('Vulpecula')),
)


@python_2_unicode_compatible
class Star(models.Model):
    """
    A variable star.
    """
    constellation = models.CharField(
        _("Constellation"), max_length=3, choices=CONSTELLATIONS, db_index=True
    )
    name = models.CharField(_("Name"), max_length=20, db_index=True)
    ra = models.CharField(_("Right Ascension"), max_length=15, default='')
    dec = models.CharField(_("Declination"), max_length=15, default='')
    variable_type = models.CharField(
        _("Type of variability"), max_length=15, default=''
    )
    max_magnitude = models.FloatField(_("Maximum brightness"), null=True)
    min_magnitude = models.FloatField(_("Minimum brightness"), null=True)
    epoch = models.FloatField(_("Epoch"), null=True)
    period = models.FloatField(_("Period"), null=True)

    class Meta:
        verbose_name = _("Variable star")
        verbose_name_plural = _("Variable stars")
        ordering = ('constellation', 'name',)

    def __str__(self):
        return self.name
