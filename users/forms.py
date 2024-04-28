from django import forms

from users.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(initial='alexneovic@gmail.com')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        try:
            user = User.objects.get(email=self.cleaned_data['email'])

            if user.check_password(self.cleaned_data['password']):
                return self.cleaned_data
            else:
                self.add_error('password',  forms.ValidationError('Password is wrong'))
        except User.DoesNotExist:
            self.add_error('email', forms.ValidationError('User does not exist'))

