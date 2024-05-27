import os

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import translation
from django.views.generic import FormView, DetailView, UpdateView

from users.forms import LoginForm, SignupForm
from users.mixins import LoggedOutOnlyView, LoggedInOnlyView, OnlyUserEmailCanChangePassword
from users.models import User


class LoginView(LoggedOutOnlyView, SuccessMessageMixin, FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('core:home')
    success_message = f'Welcome back'

    def get_success_url(self):
        next_page = self.request.GET.get('next', None)
        if next_page is not None:
            return next_page
        return self.request.user.get_absolute_url()

    def form_valid(self, form):
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super(LoginView, self).form_valid(form)


class LogOutView(LoggedInOnlyView, LogoutView):
    next_page = reverse_lazy('core:home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'See you!')
        logout(request)
        return super(LogOutView, self).dispatch(request, *args, **kwargs)


class SignupView(LoggedOutOnlyView, FormView):
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('core:home')
    initial = {}

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)
        form.fields['first_name'].widget.attrs['placeholder'] = 'Your first name'
        form.fields['last_name'].widget.attrs['placeholder'] = 'Your last name'
        form.fields['email'].widget.attrs['placeholder'] = 'Your email'
        form.fields['password'].widget.attrs['placeholder'] = 'Set your password here'
        form.fields['password1'].label = 'Confirm password'
        form.fields['password1'].widget.attrs = {
            'label': 'Confirm your password',
            'placeholder': 'Confirm your password here',

        }
        return form

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


class ProfileUpdateView(LoggedInOnlyView, UpdateView):
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


class ChangePasswordView(LoggedInOnlyView, OnlyUserEmailCanChangePassword, PasswordChangeView):
    template_name = 'users/change-password.html'
    success_url = reverse_lazy('users:user-profile-edit')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been updated!')
        form.save()
        return super().form_valid(form)


@login_required
def switch_hosting(request):
    try:
        del request.session['is_hosting']
    except KeyError:
        request.session['is_hosting'] = True
    return redirect(reverse_lazy('core:home'))


def switch_language(request):
    response = HttpResponse(status=200)
    lang = request.GET.get('lang')
    if lang is not None:
        translation.activate(lang)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)

    return response
