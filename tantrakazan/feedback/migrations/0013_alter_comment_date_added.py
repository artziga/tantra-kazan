# Generated by Django 4.2.2 on 2023-09-05 16:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0012_alter_comment_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 5, 19, 48, 12, 792343), verbose_name='дата создания'),
        ),
    ]
