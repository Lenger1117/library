import json
import csv
import os.path
from django.core.management.base import BaseCommand, CommandError
from books.models import Book, Genre


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str)

    def handle(self, *args, **options):
        file_path = "data/books.json"
        try:
            if os.path.exists(file_path) is True:
                with open('data/books.json', encoding='utf-8',
                          ) as data_file_books:
                    book_data = json.loads(data_file_books.read())
                    for books in book_data:
                        Book.objects.get_or_create(**books)

            else:
                MODELS_FILES = {Book: 'books.csv', }
                for model, file in MODELS_FILES.items():
                    with open(f'/data/{file}', encoding='utf-8',
                              ) as data_file_books_2:
                        reader = csv.DictReader(data_file_books_2)
                        model.objects.bulk_create(
                            model(**data) for data in reader
                        )

            with open('data/genres.json', encoding='utf-8',
                      ) as data_file_genres:
                genres_data = json.loads(data_file_genres.read())
                for genres in genres_data:
                    Genre.objects.get_or_create(**genres)

            self.stdout.write(self.style.SUCCESS('Данные загружены'))

        except FileNotFoundError:
            raise CommandError('Файл отсутствует в директории data')