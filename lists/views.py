from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from lists.models import List
from rooms.models import Room


def save_room(request, room_pk):
    room = Room.objects.get_or_none(pk=room_pk)
    if room is not None:
        new_list, _ = List.objects.get_or_create(
            name='My favorite rooms',
            user=request.user
        )
        new_list.rooms.add(room)
    return redirect(reverse_lazy('rooms:detail', kwargs={'pk': room_pk}))
