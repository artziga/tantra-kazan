# Generated by Django 4.2.2 on 2023-10-26 18:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0056_alter_gallery_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 26, 21, 51, 19, 486284), verbose_name='дата создания'),
        ),
    ]
