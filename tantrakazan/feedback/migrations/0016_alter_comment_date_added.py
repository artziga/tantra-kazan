# Generated by Django 4.2.2 on 2023-09-05 18:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0015_alter_comment_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 5, 21, 35, 51, 798501), verbose_name='дата создания'),
        ),
    ]
