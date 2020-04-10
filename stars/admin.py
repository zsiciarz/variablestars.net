from django.contrib import admin

from .models import Star, VariabilityType


class StarAdmin(admin.ModelAdmin):
    list_display = (
        "get_constellation_display",
        "name",
        "variability_type",
        "min_magnitude",
        "max_magnitude",
    )
    list_display_links = ("name",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("variability_type")


class VariabilityTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "short_description")


admin.site.register(Star, StarAdmin)
admin.site.register(VariabilityType, VariabilityTypeAdmin)
