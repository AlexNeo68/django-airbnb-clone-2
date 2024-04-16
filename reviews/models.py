from django.db import models
from core import models as core_model


class Review(core_model.TimeStampedModel):
    review = models.TextField()

    cleanliness = models.IntegerField()
    accuracy = models.IntegerField()
    check_in = models.IntegerField()
    communication = models.IntegerField()
    location = models.IntegerField()
    value = models.IntegerField()

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'{self.review} - {self.room}'

    def avg_rating(self):
        return round((
                             self.cleanliness +
                             self.accuracy +
                             self.check_in +
                             self.communication +
                             self.location +
                             self.value
                     ) / 6, 2)

    avg_rating.short_description = 'AVG.'
