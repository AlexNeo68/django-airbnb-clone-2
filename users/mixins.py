from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to')
        return redirect('core:home')
