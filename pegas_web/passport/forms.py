from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from .models import *


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={
            
            'class': 'Textinput-Control',
            'placeholder': 'Имя пользователя', 
            'id': 'passp-field-login',
            'name':'login'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'Textinput-Control',
            'placeholder': '',
            'id': 'passp-field-passwd',
            'name':'passwd',
            'placeholder':'* * * * * * * *'
        }
))