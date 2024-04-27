from django.shortcuts import render
from django.views.generic import View

from users.forms import LoginForm


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, 'users/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST or None)
        context = {
            "form": form
        }
        return render(request, 'users/login.html', context)
