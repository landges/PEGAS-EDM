from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from django.db.models import fields
from .models import *


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            "username": forms.TextInput(attrs={"class":"Textinput-Control","id":"login","name":"login","placeholder":"Придумайте логин"}),
            "first_name": forms.TextInput(attrs={"class":"Textinput-Control","id":"firstname","name":"firstname","placeholder":"Имя"}),
            "last_name": forms.TextInput(attrs={"class":"Textinput-Control","id":"secondname","name":"secondname","placeholder":"Фамилия"}),
            "password1": forms.TextInput(attrs={"class":"Textinput-Control","id":"password","name":"password1","placeholder":"Придумайте пароль"}),
            "password2": forms.PasswordInput(attrs={"class":"Textinput-Control","id":"password","name":"password2","placeholder":"Повторите пароль"}),
        }
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs = {"class":"Textinput-Control","id":"password","name":"password1","placeholder":"Придумайте пароль"}
        self.fields['password2'].widget.attrs = {"class":"Textinput-Control","id":"password","name":"password1","placeholder":"Придумайте пароль"}
            

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('patronomic','phone','user')
        widgets = {
            "patronomic": forms.TextInput(attrs={"class":"Textinput-Control","id":"patronomic","name":"patronomic","placeholder":"Отчество"}),
            "phone": forms.TextInput(attrs={"class":"Textinput-Control","type":"tel","id":"phone","name":"phone","placeholder":"Номер мобильного телефона"}),            
        }

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