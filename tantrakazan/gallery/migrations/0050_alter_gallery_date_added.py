# Generated by Django 4.2.2 on 2023-10-21 06:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0049_alter_gallery_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 21, 9, 49, 34, 637806), verbose_name='дата создания'),
        ),
    ]
