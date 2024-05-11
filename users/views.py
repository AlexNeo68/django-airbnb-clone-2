import os

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, DetailView, UpdateView

from users.forms import LoginForm, SignupForm
from users.models import User


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Welcome back {user.first_name}')
        return super(LoginView, self).form_valid(form)


class LogOutView(LogoutView):
    next_page = reverse_lazy('core:home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'See you!')
        logout(request)
        return super(LogOutView, self).dispatch(request, *args, **kwargs)


class SignupView(FormView):
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('core:home')
    initial = {
        "first_name": "John",
        "last_name": "Doe",
        'email': 'alexneovic@gmail.com',
    }

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Welcome back {user.first_name}')
        user.verify_email()

        return super().form_valid(form)


def complete_verification(request, secret):
    try:
        user = User.objects.get(email_secret=secret)
        user.email_verified = True
        user.email_secret = ''
        user.save()
    except User.DoesNotExist:
        return HttpResponse(status=404)

    return redirect(reverse('core:home'))


def github_login(request):
    try:
        client_id = os.environ.get('GITHUB_CLIENT_ID')
        redirect_uri = 'http://127.0.0.1:8000/users/login/github/callback/'
        scope = 'read:user'
        github_url = f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'
    except GithubException as e:
        messages.error(request, 'error with login github')
        return redirect(reverse('users:login'))

    return redirect(github_url)


class GithubException(Exception):
    pass


def github_callback(request):
    code = request.GET.get('code')

    try:

        if code is not None:
            client_id = os.environ.get('GITHUB_CLIENT_ID')
            client_secret = os.environ.get('GITHUB_CLIENT_SECRET')

            url = f'https://github.com/login/oauth/access_token'
            headers = {'Accept': 'application/json'}
            payload = {'code': code, 'client_id': client_id, 'client_secret': client_secret}
            result = requests.post(url, headers=headers, data=payload)
            result_json = result.json()
            error = result_json.get('error', None)
            if error is not None:
                raise GithubException("Github error: {}".format(error))
            else:
                access_token = result_json.get('access_token', None)
                if access_token is not None:
                    url = f'https://api.github.com/user'
                    headers = {'Authorization': f'Bearer {access_token}'}
                    profile_request = requests.get(url, headers=headers)
                    profile_json = profile_request.json()
                    username = profile_json.get('login', None)
                    if username is not None:
                        email = profile_json.get('email', None)

                        try:
                            user = User.objects.get(email=email)
                            if user.login_type != User.LOGIN_GITHUB:
                                raise GithubException(f'User login type not correct, please with email {email}')
                        except User.DoesNotExist:
                            name = profile_json.get('name', None)
                            bio = profile_json.get('bio', None)
                            user = User.objects.create(
                                username=email,
                                email=email,
                                first_name=name,
                                bio=bio,
                                login_type=User.LOGIN_GITHUB
                            )
                            user.set_unusable_password()
                            user.save()

                        login(request, user)
                        messages.success(request, f'Welcome back {user.first_name}!')
                        return redirect(reverse('core:home'))
                    else:
                        raise GithubException('Username is empty')
                else:
                    raise GithubException('Invalid token')
        else:
            raise GithubException('Code is empty')
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse('users:login'))


class ProfileView(DetailView):
    model = User
    context_object_name = 'obj_user'


class ProfileUpdateView(UpdateView):
    model = User
    fields = [
        'first_name',
        'last_name',
        'email',
        'bio',
        'gender',
        'avatar',
        'birthday',
        'currency',
        'language',
    ]
    template_name = 'users/profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user
