"""Определяет схемы URL для пользователей"""

from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    # Включить URL авторизации по умолчанию
    path('', include('django.contrib.auth.urls')),
    # Страница регистрации
    path('register/', views.register, name = 'register'),
    # Авторизация
    #path('login/', views.LoginView.as_view(), name='login'), 
    # Выход
    #path('logout/', views.LogoutView.as_view(), name='logout'), 
    # Смена пароля
    #path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # Сообщение об успешном изменении пароля
    #path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # Восстановление пароля
    #path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # Сообщение об отправке ссылки для восстановления пароля
    #path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # Вход по ссылке для восстановления пароля
    #path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # Сообщение об успешном восстановлении пароля
    #path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
