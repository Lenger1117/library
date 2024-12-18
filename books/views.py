from django.shortcuts import render
from .models import Genre, Book
from .forms import BookForm


def index(request):
    """Домашняя страница приложения Библиотека"""
    return render(request, 'books/index.html')

def genres(request):
    """Выводит список жанров."""
    genres = Genre.objects.order_by('name')
    context = {'genres': genres}
    return render(request, 'books/genres.html', context)

def genre(request, genre_id):
    """Выводит один жанр и список книг по этому жанру."""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = BookForm()
    images = Book.objects.all()

    genre = Genre.objects.get(id=genre_id)
    books = genre.book_set.order_by('name') 
    context = {'genre': genre, 'books': books, 'form': form, 'images': images}
    return render(request, 'books/genre.html', context)
