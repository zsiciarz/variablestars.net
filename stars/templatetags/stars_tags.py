from django import template
from django.utils.safestring import mark_safe

import ephem


register = template.Library()


@register.filter
def round_degrees(angle):
    """
    Rounds given angle to integer degrees.

    :param angle: an instance of ephem.Angle class
    """
    return int(round(angle / ephem.degree))


@register.simple_tag(takes_context=True)
def magnitude(context, value):
    """
    Grays out magnitude value if it is below current observer's limit.
    """
    observer = context.get('current_observer')
    if not observer:
        return value
    if value > observer.limiting_magnitude:
        return mark_safe('<span class="text-muted">%s</span>' % value)
    else:
        return value
