from django.db import models
from django.utils import timezone
from core import models as core_models

class Reservation(core_models.TimeStampedModel):
    """Model for reservation room"""

    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELED, 'Canceled'),
    )

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
    guest = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.room} - {self.check_in}'

    def in_progress(self):
        now = timezone.now()
        return self.check_in <= now <= self.check_out
    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now()
        return now > self.check_out
    is_finished.boolean = True
