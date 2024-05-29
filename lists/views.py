from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from lists.models import List
from rooms.models import Room


@login_required
def toggle_room(request, room_pk):
    room = Room.objects.get_or_none(pk=room_pk)
    if room is not None:
        new_list, created = List.objects.get_or_create(
            name='My favorite rooms',
            user=request.user
        )
        if room in new_list.rooms.all():
            new_list.rooms.remove(room)
        else:
            new_list.rooms.add(room)
    return redirect(reverse_lazy('rooms:detail', kwargs={'pk': room_pk}))


class ListDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'lists/list_detail.html'
