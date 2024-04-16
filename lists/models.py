from django.db import models

from core.models import TimeStampedModel


class List(TimeStampedModel):
    name = models.CharField(max_length=140)
    rooms = models.ManyToManyField('rooms.Room', blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='lists')

    def __str__(self):
        return self.name
