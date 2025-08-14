from django import forms
from .models import Book, Author

class BookForm(forms.ModelForm):
    authors = forms.CharField(
        label = "Авторы",
        widget = forms.TextInput(attrs={'placeholder': 'Введите имена авторов через запятую'}),
        help_text= "Если автора нет в базе данных, он будет создан автоматически"
    )

    class Meta:
        model = Book
        fields = ['name', 'authors', 'description', 'year_of_issue', 'availability', 'genres', 'image',]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Переопределяем метод __init__, чтобы предзаполнить поле authors.
        """
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Если книга уже существует (режим редактирования)
            # Преобразуем список авторов в строку через запятую
            self.initial['authors'] = ', '.join(self.instance.authors.values_list('name', flat=True))
            
    def clean_authors(self):
        author_names = self.cleaned_data['authors'].split(',')
        authors = []
        for name in author_names:
            name = name.strip()
            if name:
                author, created = Author.objects.get_or_create(name=name)
                authors.append(author)
        return authors