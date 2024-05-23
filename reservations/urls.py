from django.urls import path

from .views import ReservationDetailView, create

app_name = 'reservations'

urlpatterns = [
    path('create/<int:room_id>/<int:year>-<int:month>-<int:day>/', create, name='create'),
    path('<int:pk>/', ReservationDetailView.as_view(), name='detail'),
]