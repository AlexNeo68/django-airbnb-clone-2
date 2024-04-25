from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django_countries import countries

from rooms.models import Room, RoomType


def room_details(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/room_detail.html', context={'room': room})


class RoomDetailView(DetailView):
    model = Room


def search(request):
    city = request.GET.get('city')
    city = str.capitalize(city)
    room_types = RoomType.objects.all()
    context = {
        'city': city,
        'countries': countries,
        'room_types': room_types,
    }
    return render(request, 'rooms/search.html', context)
