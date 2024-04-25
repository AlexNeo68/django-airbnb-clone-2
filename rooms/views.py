from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django_countries import countries

from rooms.models import Room, RoomType, Amenity, Facility


def room_details(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/room_detail.html', context={'room': room})


class RoomDetailView(DetailView):
    model = Room


def search(request):
    city = request.GET.get('city', '')
    city = str.capitalize(city)
    country = request.GET.get('country', '')
    room_type = int(request.GET.get('room_type', 0))
    guests = int(request.GET.get('guests', 0))
    beds = int(request.GET.get('beds', 0))
    bedrooms = int(request.GET.get('bedrooms', 0))
    baths = int(request.GET.get('baths', 0))
    s_amenities = request.GET.getlist('amenities', [])
    s_facilities = request.GET.getlist('facilities', [])
    s_instant_book = request.GET.getlist('instant_book', 0)

    room_types = RoomType.objects.all()
    amenities = Amenity.objects.all()
    facilities = Facility.objects.all()

    choices = {
        'countries': countries,
        'room_types': room_types,
        'amenities': amenities,
        'facilities': facilities,
        's_instant_book': s_instant_book,
    }

    selected = {
        's_city': city,
        's_country': country,
        's_room_type': room_type,
        's_guests': guests,
        's_beds': beds,
        's_bedrooms': bedrooms,
        's_baths': baths,
        's_amenities': s_amenities,
        's_facilities': s_facilities,
    }
    filters = {}

    if city:
        filters['city__startswith'] = city

    if country:
        filters['country'] = country

    if room_type:
        filters['room_type__pk'] = room_type

    print(filters)

    rooms = Room.objects.filter(**filters)

    context = {**selected, **choices, 'rooms': rooms}

    return render(request, 'rooms/search.html', context)
