from django.contrib import admin

from reservations.models import Reservation, BookedDay


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('room', 'check_in', 'check_out', 'status', 'in_progress', 'is_finished')


@admin.register(BookedDay)
class BookedDayAdmin(admin.ModelAdmin):
    pass
