# Generated by Django 5.1 on 2024-11-20 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_book_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='picture',
        ),
        migrations.AddField(
            model_name='author',
            name='picture',
            field=models.ImageField(null=True, upload_to='authors', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='publishinghouse',
            name='picture',
            field=models.ImageField(null=True, upload_to='publishingHouses', verbose_name='Изображение'),
        ),
    ]
