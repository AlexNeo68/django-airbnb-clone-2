from django import forms

from users.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(initial='hmatthews@example.com')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        try:
            user = User.objects.get(email=self.cleaned_data['email'])

            if user.check_password(self.cleaned_data['password']):
                return self.cleaned_data
            else:
                self.add_error('password', forms.ValidationError('Password is wrong'))
        except User.DoesNotExist:
            self.add_error('email', forms.ValidationError('User does not exist'))


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=140)
    last_name = forms.CharField(max_length=140)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            self.add_error('email', forms.ValidationError('User already exists'))
        return email

    def clean_password1(self):
        password = self.cleaned_data['password']
        password1 = self.cleaned_data['password1']
        if password != password1:
            self.add_error('password', forms.ValidationError('Confirm your password'))
        return password

    def save(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
