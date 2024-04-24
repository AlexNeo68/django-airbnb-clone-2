from django.shortcuts import render, redirect

from rooms.models import Room


def room_details(request, pk):
    try:
        room = Room.objects.get(id=pk)
        return render(request, 'rooms/room_detail.html', context={'room': room})
    except Room.DoesNotExist:
        return redirect('core:home')
