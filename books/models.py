from django.db import models
import datetime
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название жанра', unique=True)
    color = models.CharField(max_length=7, verbose_name='Цвет')
    slug = models.SlugField(max_length=200, verbose_name='Slug', unique=True)

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """Книги в библиотеке"""
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название книги')
    author = models.CharField(max_length=200, verbose_name='Автор')
    description = models.TextField(verbose_name='Описание')
    year_of_issue = models.IntegerField(validators=[MinValueValidator(4), MaxValueValidator(datetime.datetime.now().year)], verbose_name='Год выпуска')
    availability = models.IntegerField(validators=[MaxValueValidator(100)], verbose_name='Наличие в библиотеке')
    image = models.ImageField(upload_to='books/image/', blank=True, null=True, verbose_name='Изображение')
    genres = models.ManyToManyField(Genre, blank=True, verbose_name='Жанры')
    
    class Meta:
        ordering = ('-name',)
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.name




class GenregBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')

    class Meta:
        constraints = [UniqueConstraint
                       (fields=['book', 'genre'],
                        name='book_genre_unique')]