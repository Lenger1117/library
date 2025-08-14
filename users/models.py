from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    patronymic = models.CharField(max_length=150, blank=True, null=True, verbose_name="Отчество")

    def __str__(self):
        return f"{self.user.first_name}"