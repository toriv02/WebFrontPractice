# Generated by Django 5.1 on 2024-10-10 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_rename_author_name_author_name_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Publishing_house',
            new_name='PublishingHouse',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='publishing_house',
            new_name='publishingHouse',
        ),
    ]
