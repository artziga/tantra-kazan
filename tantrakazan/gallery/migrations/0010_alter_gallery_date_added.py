# Generated by Django 4.2.2 on 2023-08-08 20:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0009_alter_gallery_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 8, 23, 27, 35, 438817), verbose_name='дата создания'),
        ),
    ]
