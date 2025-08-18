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
    path('add-book/', views.add_book, name='add_book'),
    path('book/<slug:book_slug>/edit', views.edit_book, name='edit_book'),
    path('book/<slug:book_slug>/add-review/', views.add_review, name='add_review'),
]