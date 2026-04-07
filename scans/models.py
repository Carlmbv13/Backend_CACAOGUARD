from django.db import models
from farms.models import Farm

class Scan(models.Model):
    SEVERITY_CHOICES = [
        ('Healthy', 'Healthy'),
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='scans')
    zone_name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='Healthy')
    confidence = models.FloatField(help_text="Confidence score 0-100")
    affected_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Square meters")
    image = models.ImageField(upload_to='scans/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.farm.name} - {self.zone_name} - {self.date}"
    
    class Meta:
        ordering = ['-date']