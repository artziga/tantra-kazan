# Generated by Django 4.2.2 on 2023-10-21 06:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0035_alter_comment_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 21, 9, 28, 38, 407070), verbose_name='дата создания'),
        ),
    ]
