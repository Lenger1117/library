from django.contrib import admin

from .models import Book, Genre


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'description',
                    'year_of_issue', 'availability')
    search_fields = ('name', 'author', 'genres')
    list_filter = ('name', 'author', 'genres')
    empty_value_display = '-пусто-'

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', )
    empty_value_display = '-пусто-'

admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)