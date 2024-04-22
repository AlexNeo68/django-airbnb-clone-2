from django.urls import path

from .views import all_rooms
from rooms.models import Room

app_name = 'core'

urlpatterns = [
    path('', all_rooms, name='home')
]