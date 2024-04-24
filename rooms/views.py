from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from rooms.models import Room


def room_details(request, pk):

    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/room_detail.html', context={'room': room})

