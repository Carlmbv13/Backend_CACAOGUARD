from django.db import models
from farms.models import Farm

class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='alerts')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_severity_display()}: {self.message[:50]}"
    
    class Meta:
        ordering = ['-created_at']