from django.urls import path
from .views import RoomDetailView, SearchView

app_name = 'rooms'

urlpatterns = [
    path('<int:pk>', RoomDetailView.as_view(), name='detail'),
    path('search/', SearchView.as_view(), name='search'),
]