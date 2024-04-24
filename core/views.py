from math import ceil

from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.views.generic import ListView

from rooms.models import Room


class RoomListView(ListView):
    model = Room
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = 'rooms'


def all_rooms(request):
    page = request.GET.get('page', 1)
    page = int(page or 1)
    limit = request.GET.get('limit', 10)
    limit = int(limit or 10)

    rooms = Room.objects.all()
    paginator = Paginator(rooms, limit, orphans=5)

    try:
        rooms_list = paginator.page(page)
        context = {
            'page': rooms_list,
        }
        return render(request, 'rooms/room_list.html', context)
    except EmptyPage:
        return redirect('/')
