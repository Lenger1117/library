from django.contrib import admin

from .models import Book, Genre, Author, AuthorBook, GenreBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',
                    'year_of_issue', 'availability',
                    'time_create', 'get_genres', 'get_authors')
    search_fields = ('name', 'genres')
    list_filter = ('name', 'genres')
    filter_horizontal = ['genres']
    empty_value_display = '-пусто-'

    def get_genres(self, obj):
        return ', '.join([
            genres.name for genres
            in obj.genres.all()])
    get_genres.short_description = 'Жанры'

    def get_authors(self, obj):
        return ', '.join([
            authors.name for authors
            in obj.authors.all()])
    get_authors.short_description = 'Авторы'

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', )
    empty_value_display = '-пусто-'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', )
    empty_value_display = '-пусто-'

@admin.register(GenreBook)
class GenreBook(admin.ModelAdmin):
    pass

@admin.register(AuthorBook)
class AuthorBook(admin.ModelAdmin):
    pass

class AuthorBookInline(admin.TabularInline):
    model = AuthorBook
    extra = 1
