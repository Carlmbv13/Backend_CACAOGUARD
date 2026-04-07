from django.db import models
from django.contrib.auth.models import User

class Farm(models.Model):
    RISK_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    location = models.CharField(max_length=500)
    size_hectares = models.DecimalField(max_digits=10, decimal_places=2)
    health_score = models.FloatField(default=100.0, help_text="0-100")
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES, default='Low')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']