# Generated by Django 4.2.2 on 2023-08-08 20:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_alter_gallery_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 8, 23, 23, 22, 160113), verbose_name='дата создания'),
        ),
    ]