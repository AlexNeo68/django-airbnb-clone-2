from django.urls import path
from .views import RoomDetailView, SearchView, UpdateRoomView, RoomPhotosView

app_name = 'rooms'

urlpatterns = [
    path('<int:pk>', RoomDetailView.as_view(), name='detail'),
    path('<int:pk>/photos/', RoomPhotosView.as_view(), name='photos'),
    path('<int:pk>/edit/', UpdateRoomView.as_view(), name='edit'),
    path('search/', SearchView.as_view(), name='search'),
]