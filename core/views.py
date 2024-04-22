from django.http import HttpResponse
from django.shortcuts import render

from rooms.models import Room


def all_rooms(request):
    rooms = Room.objects.all()
    hungry = False
    context = {
        'rooms': rooms,
        'hungry': hungry
    }
    return render(request, 'rooms/index.html', context)
