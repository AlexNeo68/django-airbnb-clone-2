from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django_countries import countries

from rooms.forms import SearchForm
from rooms.models import Room, RoomType, Amenity, Facility


def room_details(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/room_detail.html', context={'room': room})


class RoomDetailView(DetailView):
    model = Room


def search(request):

    form = SearchForm(request.GET)

    context = {"search_form": form}

    return render(request, 'rooms/search.html', context)
