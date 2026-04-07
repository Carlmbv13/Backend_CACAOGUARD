from django.contrib import admin
from .models import Scan

@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ['farm', 'zone_name', 'severity', 'confidence', 'affected_area', 'date']
    list_filter = ['severity', 'date']
    search_fields = ['farm__name', 'zone_name']
    readonly_fields = ['date', 'created_at']