from django.urls import path

from .views import toggle_room, ListDetailView

app_name = 'lists'

urlpatterns = [

    path('add/<int:room_pk>', toggle_room, name='toggle-room'),
    path('faves/', ListDetailView.as_view(), name='list-detail'),


]