# Generated by Django 4.2.2 on 2023-12-01 19:29

import autoslug.fields
import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='название')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True, verbose_name='слаг')),
                ('text', ckeditor.fields.RichTextField(verbose_name='Текст статьи')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='дата редактирования')),
            ],
            options={
                'verbose_name': 'статья',
                'verbose_name_plural': 'статьи',
                'ordering': ['-last_update', '-pk'],
                'get_latest_by': 'last_update',
            },
        ),
    ]