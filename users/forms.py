from django import forms

from users.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        try:
            user = User.objects.get(email=self.cleaned_data['email'])

            if user.check_password(self.cleaned_data['password']):
                return self.cleaned_data
            else:
                self.add_error('password', forms.ValidationError('Password is wrong'))
        except User.DoesNotExist:
            self.add_error('email', forms.ValidationError('User does not exist'))


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            self.add_error('email', forms.ValidationError('Email already exists', code='existing user'))
        else:
            return email

    def clean_password1(self):
        password = self.cleaned_data['password']
        password1 = self.cleaned_data['password1']
        if password != password1:
            self.add_error('password', forms.ValidationError('Confirm your password'))
        return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        user.save()
