# Generated by Django 3.2.25 on 2025-07-07 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20250701_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(default='default-slug', max_length=200, unique=True, verbose_name='Slug_book'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='Slug_genre'),
        ),
    ]
