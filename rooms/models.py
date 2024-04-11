from django.db import models

from core.models import TimeStampedModel
from users.models import User
from django_countries.fields import CountryField


class Room(TimeStampedModel):
    
    """Model for Room entity"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=140)
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bathrooms = models.IntegerField()
    price = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False) #занято ли
    host = models.ForeignKey(User, on_delete=models.CASCADE) #владелец
