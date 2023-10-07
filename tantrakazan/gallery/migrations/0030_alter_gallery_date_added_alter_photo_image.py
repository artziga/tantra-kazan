# Generated by Django 4.2.2 on 2023-09-11 18:21

import datetime
from django.db import migrations, models
import gallery.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0029_alter_photo_options_remove_photo_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 11, 21, 21, 56, 392067), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=gallery.models.get_storage_path, verbose_name='фото'),
        ),
    ]