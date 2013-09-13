from __future__ import unicode_literals

from django.contrib import admin

from .models import Star


class StarAdmin(admin.ModelAdmin):
    list_display = (
        'get_constellation_display', 'name', 'variable_type',
        'min_magnitude', 'max_magnitude',
    )
    list_display_links = ('name',)


admin.site.register(Star, StarAdmin)
