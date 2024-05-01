from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from users.forms import LoginForm, SignupForm


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
        return super(LoginView, self).form_valid(form)


class LogOutView(LogoutView):
    next_page = reverse_lazy('core:home')
    # template_name = 'users/logout.html'


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
        user.verify_email()
        return super().form_valid(form)
