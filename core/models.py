from django.db import models

# Create your models here.

class TimeStampedModel(models.Model):
    """Abstract class with fields created and updated"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
