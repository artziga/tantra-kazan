# Generated by Django 4.2.2 on 2023-09-06 18:39

import autoslug.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0028_alter_gallery_date_added_alter_photo_upload_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'get_latest_by': 'upload_date', 'ordering': ['-upload_date', '-pk'], 'verbose_name': 'фото'},
        ),
        migrations.RemoveField(
            model_name='photo',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='gallery',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 6, 21, 39, 34, 663215), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True, verbose_name='слаг'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True, verbose_name='слаг'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
