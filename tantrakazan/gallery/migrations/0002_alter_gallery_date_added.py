# Generated by Django 4.2.2 on 2023-08-23 17:08

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
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 23, 20, 8, 37, 566041), verbose_name='дата создания'),
        ),
    ]
