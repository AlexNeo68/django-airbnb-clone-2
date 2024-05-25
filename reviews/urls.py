from django.urls import path

from reviews.views import create

app_name = 'reviews'

urlpatterns = [
    path('create/<int:room_id>/', create, name='review-create')
]