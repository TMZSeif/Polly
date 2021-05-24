from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from poll.models import MyUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']
        