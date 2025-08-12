"""Определяет схемы URL для Книг."""

from django.urls import path
from . import views


app_name = 'books'
urlpatterns = [
    path('', views.index, name='index'),
    path('genres/', views.genres, name='genres'),
    path('book/<slug:book_slug>/', views.book, name='book'),
    path('genre/<slug:genre_slug>/', views.genre, name='genre'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorite/<slug:book_slug>/', views.favorite, name='favorite'),
]