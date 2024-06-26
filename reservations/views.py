import datetime

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from reservations.models import BookedDay, Reservation
from reviews.forms import ReviewForm
from rooms.models import Room


class CreateError(Exception):
    pass


def create(request, room_id, year, month, day):
    date_obj = datetime.date(int(year), int(month), int(day))
    room = None
    try:
        room = Room.objects.get(pk=int(room_id))
        BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError
    except (Room.DoesNotExist, CreateError):
        messages.error(request, 'Room does not found.')
        return redirect(reverse('core:home'))
    except BookedDay.DoesNotExist:
        reservation = Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1)
        )
        return redirect(reverse('reservations:detail', kwargs={'pk': reservation.pk}))


class ReservationDetailView(View):
    def get(self, *args, **kwargs):

        pk = kwargs['pk']
        reservation = Reservation.objects.get_or_none(pk=pk)
        # Проверка на то что разрешается сюда зайди только гостю который сделал резерв, или владельцу комнаты
        if not reservation or (reservation.guest != self.request.user and reservation.room.host != self.request.user):
            raise Http404
        form = ReviewForm()
        context = {
            'reservation': reservation,
            'form': form,
        }
        return render(self.request, 'reservations/detail.html', context)



def edit_reservation(request, pk, verb):
    reservation = Reservation.objects.get_or_none(pk=pk)
    if not reservation or (reservation.guest != request.user and reservation.room.host != request.user):
        raise Http404

    if verb == 'cancel':
        reservation.status = Reservation.STATUS_CANCELED
        BookedDay.objects.filter(reservation=reservation).delete()
    if verb == 'confirm':
        reservation.status = Reservation.STATUS_CONFIRMED

    reservation.save()

    messages.success(request, 'Reservation updated!')
    return redirect(reverse('reservations:detail', kwargs={'pk': reservation.pk}))



