from django.urls import path
from .views import RoomDetailView, SearchView, UpdateRoomView, RoomPhotosView, photo_delete

app_name = 'rooms'

urlpatterns = [
    path('<int:pk>', RoomDetailView.as_view(), name='detail'),
    path('<int:pk>/photos/', RoomPhotosView.as_view(), name='photos'),
    path('<int:room_pk>/photos/<int:photo_pk>/remove/', photo_delete, name='photo-remove'),
    path('<int:pk>/edit/', UpdateRoomView.as_view(), name='edit'),
    path('search/', SearchView.as_view(), name='search'),
]