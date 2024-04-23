from math import ceil

from django.core.paginator import Paginator
from django.shortcuts import render

from rooms.models import Room


def all_rooms(request):
    page = request.GET.get('page', 1)
    page = int(page or 1)
    limit = request.GET.get('limit', 10)
    limit = int(limit or 10)

    rooms = Room.objects.all()
    paginator = Paginator(rooms, limit, orphans=5)

    rooms_list = paginator.get_page(page)

    print(vars(rooms_list))

    context = {
        'page': rooms_list,
    }
    return render(request, 'rooms/index.html', context)
