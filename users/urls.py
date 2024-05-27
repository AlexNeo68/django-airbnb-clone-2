from django.urls import path

from .views import (LoginView, LogOutView, SignupView, complete_verification, github_login, github_callback,
                    ProfileView, ProfileUpdateView, ChangePasswordView, switch_hosting, switch_language)

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/github/', github_login, name='login-github'),
    path('login/github/callback/', github_callback, name='login-github-callback'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify/<str:secret>', complete_verification, name='complete_verification'),
    path('profile-edit/', ProfileUpdateView.as_view(), name='user-profile-edit'),
    path('change-password/', ChangePasswordView.as_view(), name='user-change-password'),
    path('switch-hosting/', switch_hosting, name='user-switch-hosting'),
    path('switch-language/', switch_language, name='user-switch-language'),
    path('<int:pk>/', ProfileView.as_view(), name='user-profile'),
]