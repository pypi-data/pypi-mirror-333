# apps/api_management/models.py
from django.db import models
from apps.payments.models import Plan

class ApiService(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ApiRoute(models.Model):
    service = models.ForeignKey(ApiService, on_delete=models.CASCADE, related_name='routes')
    path = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.path})"

class ApiPlan(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    service = models.ForeignKey(ApiService, on_delete=models.CASCADE)
    rate_limit = models.IntegerField(help_text="Requests per minute")
    
    class Meta:
        unique_together = ['plan', 'service']