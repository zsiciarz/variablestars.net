from django.contrib import admin

from .models import Observer


class ObserverAdmin(admin.ModelAdmin):
    list_display = ('user', 'aavso_code',)
    list_display_links = ('user',)


admin.site.register(Observer, ObserverAdmin)
