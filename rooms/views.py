from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, View

from rooms.forms import SearchForm
from rooms.models import Room


def room_details(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/room_detail.html', context={'room': room})


class RoomDetailView(DetailView):
    model = Room


class SearchView(View):

    def get(self, request):
        filters = {}

        country = request.GET.get('country')
        if country:
            form = SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data['city']
                country = form.cleaned_data['country']
                price = form.cleaned_data['price']
                guests = form.cleaned_data['guests']
                beds = form.cleaned_data['beds']
                bedrooms = form.cleaned_data['bedrooms']
                baths = form.cleaned_data['baths']
                amenities = form.cleaned_data['amenities']
                facilities = form.cleaned_data['facilities']
                room_type = form.cleaned_data['room_type']
                instant_book = form.cleaned_data['instant_book']

                if city:
                    filters['city__startswith'] = city

                if country:
                    filters['country'] = country

                if room_type:
                    filters['room_type'] = room_type

                if price:
                    filters['price__lte'] = price

                if guests:
                    filters['guests__gte'] = guests

                if beds:
                    filters['beds__gte'] = beds

                if bedrooms:
                    filters['bedrooms__gte'] = bedrooms

                if baths:
                    filters['baths__gte'] = baths

                if len(amenities) > 0:
                    for amenity in amenities:
                        filters['amenities'] = amenity

                if len(facilities) > 0:
                    for facility in facilities:
                        filters['facilities'] = facility

                if instant_book:
                    filters['instant_book'] = True

                qs = Room.objects.filter(**filters).order_by('-created')

                paginator = Paginator(qs, 5, orphans=5)

                page = request.GET.get('page', 1)

                print(page)

                rooms = paginator.get_page(page)

                context = {"search_form": form, 'rooms': rooms}

                return render(request, 'rooms/search.html', context)

        else:
            form = SearchForm()
            context = {"search_form": form}
            return render(request, 'rooms/search.html', context)




def search(request):
    filters = {}

    country = request.GET.get('country')
    if country:
        form = SearchForm(request.GET)
        if form.is_valid():
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            price = form.cleaned_data['price']
            guests = form.cleaned_data['guests']
            beds = form.cleaned_data['beds']
            bedrooms = form.cleaned_data['bedrooms']
            baths = form.cleaned_data['baths']
            amenities = form.cleaned_data['amenities']
            facilities = form.cleaned_data['facilities']
            room_type = form.cleaned_data['room_type']
            instant_book = form.cleaned_data['instant_book']

            if city:
                filters['city__startswith'] = city

            if country:
                filters['country'] = country

            if room_type:
                filters['room_type'] = room_type

            if price:
                filters['price__lte'] = price

            if guests:
                filters['guests__gte'] = guests

            if beds:
                filters['beds__gte'] = beds

            if bedrooms:
                filters['bedrooms__gte'] = bedrooms

            if baths:
                filters['baths__gte'] = baths

            if len(amenities) > 0:
                for amenity in amenities:
                    filters['amenities'] = amenity

            if len(facilities) > 0:
                for facility in facilities:
                    filters['facilities'] = facility

            if instant_book:
                filters['instant_book'] = True

    else:
        form = SearchForm()

    print(filters)

    rooms = Room.objects.filter(**filters)

    context = {"search_form": form, 'rooms': rooms}

    return render(request, 'rooms/search.html', context)
