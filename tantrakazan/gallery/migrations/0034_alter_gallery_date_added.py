# Generated by Django 4.2.2 on 2023-09-30 08:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0033_alter_avatar_image_alter_gallery_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 30, 11, 38, 31, 37321), verbose_name='дата создания'),
        ),
    ]
