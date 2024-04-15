from django.db import models

from core.models import TimeStampedModel
from django_countries.fields import CountryField

class AbstractItem(TimeStampedModel):

    """Abstract Class for Models"""

    name = models.CharField(max_length=140)
    subtitle = models.TextField(blank=True, null=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class RoomType(AbstractItem):
    class Meta:
        verbose_name = 'Room Type'

class Amenity(AbstractItem):
    class Meta:
        verbose_name_plural = 'Amenities'

class Facility(AbstractItem):
    class Meta:
        verbose_name_plural = 'Facilities'

class HouseRule(AbstractItem):
    class Meta:
        verbose_name = 'House Rule'

class Photo(TimeStampedModel):
    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE)

    def __str__(self):
        return self.caption



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
    host = models.ForeignKey('users.User', on_delete=models.CASCADE) #владелец
    room_type = models.ForeignKey('RoomType', on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField('Amenity', blank=True)
    facilities = models.ManyToManyField('Facility', blank=True)
    house_rules = models.ManyToManyField('HouseRule', blank=True)

    def __str__(self):
        return self.name
