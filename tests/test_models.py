from django.test import TestCase
from books.models import Book, Author, Genre

class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Настройка данных для всех тестов в этом классе.
        """
        cls.author = Author.objects.create(name="Лев Толстой")
        cls.genre = Genre.objects.create(name="Классика", slug="klassika")
        cls.book = Book.objects.create(
            name="Война и мир",
            slug="voyna-i-mir",
            description="Эпическая история о войне и мире.",
            year_of_issue=1869,
            availability=5
        )
        cls.book.authors.add(cls.author)
        cls.book.genres.add(cls.genre)

    def test_book_creation(self):
        """
        Проверка, что книга создается корректно.
        """
        self.assertEqual(self.book.name, "Война и мир")
        self.assertEqual(self.book.slug, "voyna-i-mir")
        self.assertEqual(self.book.year_of_issue, 1869)
        self.assertEqual(self.book.availability, 5)

    def test_book_str_representation(self):
        """
        Проверка строкового представления книги.
        """
        self.assertEqual(str(self.book), "Война и мир")

    def test_book_authors(self):
        """
        Проверка связи с авторами.
        """
        self.assertIn(self.author, self.book.authors.all())

    def test_book_genres(self):
        """
        Проверка связи с жанрами.
        """
        self.assertIn(self.genre, self.book.genres.all())

    def test_book_slug_unique(self):
        """
        Проверка уникальности slug.
        """
        with self.assertRaises(Exception):
            Book.objects.create(
                name="Анна Каренина",
                slug="voyna-i-mir",  # Повторение slug
                description="История любви Анны Карениной.",
                year_of_issue=1877,
                availability=3
            )