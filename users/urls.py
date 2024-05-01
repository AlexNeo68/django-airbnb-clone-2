from django.urls import path

from .views import LoginView, LogOutView, SignupView, complete_verification

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify/<str:secret>', complete_verification, name='complete_verification'),
]