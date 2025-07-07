import json
from django.core.management.base import BaseCommand, CommandError
from books.models import Author, Book, Genre
import pdb


def load_books(file_path):
    with open(file_path, encoding='utf-8') as data_file:
        books_data = json.load(data_file)
        for book in books_data:
            # Извлекаем поле authors, если оно есть, и удаляем его из данных
            authors = book.pop('authors', None)

            # Создаем или получаем книгу без учета authors
            book_instance, created = Book.objects.get_or_create(**book)

            # Если authors указано, обрабатываем связь
            if authors:
                if isinstance(authors, list) and all(isinstance(a, int) for a in authors):
                    print(f"Authors for book '{book_instance.name}': {authors}")

                    # Получаем авторов по их ID
                    author_objects = Author.objects.filter(id__in=authors)

                    if not author_objects.exists():
                        print(f"Нет авторов с идентификаторами: {authors}")
                    else:
                        # Устанавливаем ManyToMany связь
                        book_instance.authors.set(author_objects)
                else:
                    print(f"Неверный формат для authors: {authors}")


def load_genres(file_path):
    with open(file_path, encoding='utf-8') as data_file:
        genres_data = json.load(data_file)
        for genre_data in genres_data:
            Genre.objects.get_or_create(**genre_data)


def load_authors(file_path):
    with open(file_path, encoding='utf-8') as data_file:
        authors_data = json.load(data_file)
        for author_data in authors_data:
            Author.objects.get_or_create(**author_data)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--path", type=str)

    def handle(self, *args, **options):
        authors_file_path = 'data/authors.json'
        books_file_path = 'data/books.json'
        genres_file_path = 'data/genres.json'
        try:
            load_authors(authors_file_path)
            load_books(books_file_path)
            load_genres(genres_file_path)
            self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))
        except FileNotFoundError:
            raise CommandError('Файл отсутствует в директории data')
        except json.JSONDecodeError:
            raise CommandError('Ошибка декодирования JSON файла')

