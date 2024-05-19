from django.urls import path
from .views import RoomDetailView, SearchView, UpdateRoomView, RoomPhotosView, photo_delete, UpdateRoomPhotoView, CreateRoomPhotoView, DeleteRoomPhotoView, CreateRoomView

app_name = 'rooms'

urlpatterns = [
    path('create/', CreateRoomView.as_view(), name='create'),
    path('<int:pk>/', RoomDetailView.as_view(), name='detail'),
    path('<int:pk>/photos/', RoomPhotosView.as_view(), name='photos'),
    path('<int:room_pk>/photos/add/', CreateRoomPhotoView.as_view(), name='photo-add'),
    path('<int:room_pk>/photos/<int:photo_pk>/remove/', DeleteRoomPhotoView.as_view(), name='photo-remove'),
    path('<int:room_pk>/photos/<int:photo_pk>/edit/', UpdateRoomPhotoView.as_view(), name='photo-edit'),
    path('<int:pk>/edit/', UpdateRoomView.as_view(), name='edit'),
    path('search/', SearchView.as_view(), name='search'),
]