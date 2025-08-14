from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Genre, Book, Author, AuthorBook, Favorite
from .forms import BookForm


def index(request):
    """Домашняя страница"""
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
    favorite_slugs = request.user.favorites.values_list('book__slug', flat=True)
    
    return render(request, 'books/genre.html', {
        'genre': genre,
        'books': books,
        'favorite_slugs': favorite_slugs
    })

def book(request, book_slug):
    """Страница конкретной книги."""
    book = get_object_or_404(Book, slug=book_slug)
    is_favorite = False

    # Проверяем, добавлена ли книга в избранное (только для авторизованных пользователей)
    if request.user.is_authenticated:
        is_favorite = book.favorites.filter(user=request.user).exists()

    return render(request, 'books/book.html', {'book': book, 'is_favorite': is_favorite})

@login_required
def favorite(request, book_slug):
    """Добавляет или удаляет книгу из списка избранного пользователя."""
    if request.method == 'POST':
        book = get_object_or_404(Book, slug=book_slug)
        user = request.user

        # Проверяем, есть ли уже эта книга в избранном
        favorite, created = Favorite.objects.get_or_create(user=user, book=book)

        if not created:
            # Если книга уже в избранном, удаляем её
            favorite.delete()
            messages.success(request, 'Книга удалена из избранного.')
        else:
            # Если книга добавлена в избранное
            messages.success(request, 'Книга добавлена в избранное.')

        # Определяем, куда перенаправлять пользователя
        referer = request.META.get('HTTP_REFERER', '/')
        if '/genre/' in referer:
            # Если пользователь находится на странице жанра
            return redirect(f'/genre/{book.genres.first().slug}/#scroll-to-here')
        elif '/book/' in referer:
            # Если пользователь находится на персональной странице книги
            return redirect(f'/book/{book.slug}/#scroll-to-here')
        elif '/favorites/' in referer:
            # Если пользователь находится на персональной странице книги
            return redirect(f'/favorites/')
        else:
            # В остальных случаях перенаправляем на главную страницу
            return redirect('/')

@login_required
def favorites(request):
    """Отображает список книг, добавленных в избранное текущим пользователем."""
    favorite_books = request.user.favorites.all()  # Получаем все избранные книги пользователя
    return render(request, 'books/favorites.html', {'favorite_books': favorite_books})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_book(request):
    """Отображение формы для добавления новой книги."""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            book.authors.set(form.cleaned_data['authors'])
            book.genres.set(form.cleaned_data['genres'])
            book.save()
            return redirect('books:book', book_slug=book.slug)
    
    else:
        form = BookForm()
    
    return render(request, 'books/add_book.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_book(request, book_slug):
    """Отображает форму для редактирования существующей книги."""
    book = get_object_or_404(Book, slug=book_slug)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:book', book_slug=book.slug)
    else:
        form = BookForm(instance=book)

    return render(request, 'books/edit_book.html', {'form': form, 'book': book})
