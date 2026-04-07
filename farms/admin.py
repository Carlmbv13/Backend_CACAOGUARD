from django.contrib import admin
from .models import Farm

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'location', 'size_hectares', 'health_score', 'risk_level', 'created_at']
    list_filter = ['risk_level', 'created_at']
    search_fields = ['name', 'owner__username', 'location']
    readonly_fields = ['created_at', 'updated_at']