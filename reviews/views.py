from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from reviews.forms import ReviewForm
from rooms.models import Room


def create(request, room_id):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        room = Room.objects.get_or_none(id=room_id)
        if not room:
            return redirect('core:home')
        if form.is_valid():
            review = form.save(commit=False)
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, 'Review successfully created')
            return redirect(reverse_lazy('rooms:detail', kwargs={'pk': room.pk}))




