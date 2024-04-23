from django.urls import path

from .views import all_rooms, RoomListView
from rooms.models import Room

app_name = 'core'

urlpatterns = [
    path('', RoomListView.as_view(), name='home')
]