from users.forms import RegisterUserForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

def register(request):
    """Регистрирует нового пользователя"""
    if request.method != 'POST':
        #Выводит пустую форму регистрации
        form = RegisterUserForm()
    else:
        #Обработка заполненной формы
        form = RegisterUserForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Выполнение входа и перенаправление на домашнюю страницу
            new_user.backend = 'users.auth_backend.EmailBackend'  # ← Это ключевая строка!
            login(request, new_user)
            return redirect('books:index')
    
    #Вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'registration/register.html', context)