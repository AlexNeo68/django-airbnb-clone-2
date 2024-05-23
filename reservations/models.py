import datetime

from django.db import models
from django.utils import timezone
from core import models as core_models
from reservations.managers import ReservationCustomerManager


class BookedDay(core_models.TimeStampedModel):
    day = models.DateField()
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, related_name='booked_days')

    class Meta:
        verbose_name = 'Booked Day'
        verbose_name_plural = 'Booked Days'

    def __str__(self):
        return str(self.day)


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

    objects = ReservationCustomerManager()

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

    def save(self, *args, **kwargs):
        if self.pk is None:
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects.filter(day__range=(start, end)).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)
