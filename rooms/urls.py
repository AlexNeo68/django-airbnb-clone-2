from django.urls import path
from .views import room_details

app_name = 'rooms'

urlpatterns = [
    path('<int:pk>', room_details, name='detail')
]