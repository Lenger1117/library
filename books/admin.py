from django.contrib import admin

from .models import Book, Genre, Author, AuthorBook, GenreBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'short_description',
                    'year_of_issue', 'availability',
                    'time_create', 'get_genres', 'get_authors')
    search_fields = ('name', 'genres')
    list_filter = ('name', 'genres')
    filter_horizontal = ['genres']
    empty_value_display = '-пусто-'

    @admin.display(description="Описание")
    def short_description(self, obj):
        return f"{obj.description[:30]}..." if obj.description else ""

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
    list_display = ('name', 'slug')
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
