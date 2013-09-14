# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Observation


class ObservationAdmin(admin.ModelAdmin):
    list_display = ('observer', 'star', 'jd', 'magnitude', 'comp1', 'notes')
    list_display_links = ('jd',)


admin.site.register(Observation, ObservationAdmin)
