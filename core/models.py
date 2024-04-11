from django.db import models

# Create your models here.

class TimeStampedModel(models.Model):
    """Abstract class with fields created and updated"""
    
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        abstract = True
