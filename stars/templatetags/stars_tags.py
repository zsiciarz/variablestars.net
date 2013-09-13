# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template

import ephem


register = template.Library()


@register.filter
def round_degrees(angle):
    """
    Rounds given angle to integer degrees.

    :param angle: an instance of ephem.Angle class
    """
    return int(round(angle / ephem.degree))
