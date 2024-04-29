from django.urls import path

from .views import LoginView, LogOutView, SignupView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]