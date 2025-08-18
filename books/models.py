from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import unique_slugify


class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя автора', unique=True)
    slug = models.SlugField(max_length=200,  verbose_name='Slug_author', unique=False, db_index=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        """Сохранение полей модели при их отсутствии заполнения."""
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название жанра', unique=True)
    color = models.CharField(max_length=7, verbose_name='Цвет')
    slug = models.SlugField(max_length=200, verbose_name='Slug_genre', unique=True, db_index=True)

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        """Сохранение полей модели при их отсутствии заполнения."""
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class Book(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название книги')
    authors = models.ManyToManyField(Author, verbose_name='Автор', through='AuthorBook', blank=True)
    description = models.TextField(verbose_name='Описание')
    year_of_issue = models.IntegerField(validators=[MinValueValidator(4), MaxValueValidator(datetime.datetime.now().year)], verbose_name='Год выпуска')
    availability = models.IntegerField(validators=[MaxValueValidator(100)], verbose_name='Наличие')
    image = models.ImageField(upload_to='books/image/', blank=True, null=True, verbose_name='Изображение')
    genres = models.ManyToManyField(Genre, blank=True, verbose_name='Жанры', through='GenreBook')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления')
    slug = models.SlugField(max_length=200, verbose_name='Slug_book', unique=True, db_index=True)
    
    class Meta:
        ordering = ('-name',)
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.name
    
    def save(self, *args, **kwargs):
        """Сохранение полей модели при их отсутствии заполнения."""
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)
    
    def average_rating(self):
        """Вычисление средней оценки книги"""
        reviews = self.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            return round(total_rating / reviews.count(), 1)
        return 0
    
    def review_count(self):
        """Возвращение кол-ва отзывов к книге"""
        return self.reviews.count()



class GenreBook(models.Model):
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, verbose_name='Книга')
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL, verbose_name='Жанр')

    class Meta:
        constraints = [UniqueConstraint
                       (fields=['book', 'genre'],
                        name='book_genre_unique')]
        verbose_name = 'Жанр-Книга'
        verbose_name_plural = 'Жанры-Книга'


class AuthorBook(models.Model):
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, verbose_name='Книга')
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        constraints = [UniqueConstraint
                       (fields=['book', 'author'],
                        name='book_author_unique')]
        verbose_name = 'Автор-Книга'
        verbose_name_plural = 'Авторы-Книга'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name='Книга',
        related_name='favorites'
    )

    class Meta:
        constraints = [UniqueConstraint(
            fields=['user', 'book'],
            name='user_favorite_unique')]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self) -> str:
        return f'{self.user} - {self.book}'


class Review(models.Model):
        book = models.ForeignKey(
            Book,
            on_delete=models.CASCADE,
            verbose_name='Книга',
            related_name='reviews'
        )
        user = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            verbose_name='Пользователь',
            related_name='reviews'
        )
        rating = models.PositiveIntegerField(
            choices = [(i, i) for i in range(1, 6)],
            verbose_name='Оценка'
        )
        comment = models.TextField(blank=True, null=True, verbose_name='Отзыв')
        created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
        class Meta:
            verbose_name = "Отзыв"
            verbose_name_plural = "Отзывы"

        def __str__(self):
            return f"Отзыв на {self.book.name} от {self.user.username}"  