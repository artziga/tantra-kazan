# Generated by Django 4.2.2 on 2023-10-21 06:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0031_alter_comment_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 21, 9, 5, 19, 704526), verbose_name='дата создания'),
        ),
    ]
