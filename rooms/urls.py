from django.urls import path
from .views import RoomDetailView, search

app_name = 'rooms'

urlpatterns = [
    path('<int:pk>', RoomDetailView.as_view(), name='detail'),
    path('search/', search, name='search'),
]