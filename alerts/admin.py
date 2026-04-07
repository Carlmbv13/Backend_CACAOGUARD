from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['farm', 'severity', 'message', 'status', 'created_at']
    list_filter = ['severity', 'status', 'created_at']
    search_fields = ['farm__name', 'message']
    readonly_fields = ['created_at', 'updated_at']