# Generated by Django 4.2.2 on 2023-08-01 12:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 15, 16, 23, 297017), verbose_name='дата создания'),
        ),
    ]
