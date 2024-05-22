import datetime

from django import template

from reservations.models import BookedDay

register = template.Library()


@register.simple_tag
def is_booked_day(room, day):

    if day.number == 0:
        return
    date = datetime.datetime(year=day.year, month=day.month, day=day.number)
    try:
        BookedDay.objects.get(day=date, reservation__room=room)
        return True
    except BookedDay.DoesNotExist:
        return False
