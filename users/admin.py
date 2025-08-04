from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile  # ← можно использовать .models


# Inline для профиля (НЕ регистрируем через @admin.register!)
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Персональные данные'


# Кастомный UserAdmin
class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]  # ← подключаем Inline сюда

    list_display = ('email', 'first_name', 'last_name', 'get_patronymic', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)

    def get_patronymic(self, obj):
        try:
            return obj.profile.patronymic or "-"
        except UserProfile.DoesNotExist:
            return "-"
    get_patronymic.short_description = 'Отчество'
    get_patronymic.admin_order_field = 'profile__patronymic'


# Регистрируем кастомного User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# А теперь — отдельно регистрируем UserProfile с полноценным ModelAdmin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'patronymic')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'patronymic')
    # autocomplete_fields = ('user',)  # раскомментируй, если много пользователей