from django.shortcuts import render
from .models import Genre, Book, Author, AuthorBook
from .forms import BookForm


def index(request):
    """Домашняя страница приложения Библиотека"""
    return render(request, 'books/index.html')

def genres(request):
    """Выводит список жанров."""
    genres = Genre.objects.order_by('name')
    context = {'genres': genres}
    return render(request, 'books/genres.html', context)

def genre(request, genre_slug):
    """Выводит один жанр и список книг по этому жанру."""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = BookForm()
    
    images = Book.objects.all()
    genre = Genre.objects.get(slug=genre_slug)
    #author = AuthorBook.author_set.all()
    books = genre.book_set.order_by('-time_create') 
    context = {'genre': genre, 'books': books, 'form': form, 'images': images}
    return render(request, 'books/genre.html', context)
