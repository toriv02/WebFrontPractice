# Generated by Django 5.1.1 on 2024-09-12 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('year_of_publication', models.TextField()),
                ('author', models.TextField()),
                ('genre', models.TextField()),
            ],
        ),
    ]
