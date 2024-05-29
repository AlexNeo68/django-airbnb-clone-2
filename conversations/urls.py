from django.urls import path

from .views import go_conversation

app_name = 'conversations'

urlpatterns = [
    path('go/<int:a_pk>/<int:b_pk>/', go_conversation, name='go')
]