from django.db import models

from core.models import TimeStampedModel


class Conversation(TimeStampedModel):
    participants = models.ManyToManyField('users.User')

    def __str__(self):
        usernames = []
        for participant in self.participants.all():
            usernames.append(participant.username)
        return ', '.join(usernames)

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = 'Number of messages'

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = 'Number of participants'


class Message(TimeStampedModel):
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f'{self.sender} says: {self.message}'
