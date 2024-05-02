from django.urls import path

from .views import LoginView, LogOutView, SignupView, complete_verification, github_login, github_callback

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/github/', github_login, name='login-github'),
    path('login/github/callback/', github_callback, name='login-github-callback'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify/<str:secret>', complete_verification, name='complete_verification'),
]