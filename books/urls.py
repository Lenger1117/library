"""Определяет схемы URL для Книг."""

from django.urls import path
from . import views


app_name = 'books'
urlpatterns = [
    # Домашняя страница
    path('', views.index, name='index'),
    # Страница со списком всех жанров
    path('genres/', views.genres, name='genres'),
    # Страница со списком книг по отдельным жанрам
    path('genre/<slug:genre_slug>/', views.genre, name='genre'),
    path('book/<slug:book_slug>/', views.genre, name='book'),
    ]