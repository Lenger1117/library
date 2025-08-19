from .models import Genre

def genres(request):
    """
    Контекстный процессор для передачи списка жанров во все шаблоны.
    """
    return {
        'genres': Genre.objects.all().order_by('name')
    }