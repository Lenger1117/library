from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действующий email.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    first_name = forms.CharField(label='Фамилия пользователя')
    last_name = forms.CharField(label='Имя пользователя')
    patronymic = forms.CharField(label='Отчество пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)