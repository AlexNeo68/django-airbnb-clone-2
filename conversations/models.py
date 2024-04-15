from django.db import models

from core.models import TimeStampedModel


class Conversation(TimeStampedModel):
    participants = models.ManyToManyField('users.User')

    def __str__(self):
        return str(self.created)


class Message(TimeStampedModel):
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE)
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f'{self.sender} says: {self.message}'
