import re
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Adres email'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @staticmethod
    def _validate_email(email):
        pattern = r'^[A-Za-z0-9._]+@' + settings.EMAIL_DOMAIN
        if re.match(pattern, email):
            return True
        return False

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user is not None or not self._validate_email(email):
            raise forms.ValidationError('Wrong email address')
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class ConfirmationForm(forms.Form):
    email = forms.EmailField()