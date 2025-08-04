from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from users.models import UserProfile

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    patronymic = forms.CharField(max_length=30, required=False, label='Отчество')
    email = forms.EmailField(required=True, label='Email')

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # ← email = username
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        # Сохраняем отчество в профиль (если есть)
        # В методе save() формы
        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'patronymic': self.cleaned_data.get('patronymic', '')}
            )
        return user

# class LoginForm(AuthenticationForm):
#     first_name = forms.CharField(label='Фамилия пользователя')
#     last_name = forms.CharField(label='Имя пользователя')
#     patronymic = forms.CharField(label='Отчество пользователя')
#     password = forms.CharField(label='Пароль', widget=forms.PasswordInput)