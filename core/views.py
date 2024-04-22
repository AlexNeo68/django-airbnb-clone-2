from django.http import HttpResponse
from django.shortcuts import render

from rooms.models import Room


def all_rooms(request):
    return HttpResponse(Room.objects.all())
