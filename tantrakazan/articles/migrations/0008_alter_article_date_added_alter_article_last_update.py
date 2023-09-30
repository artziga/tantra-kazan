# Generated by Django 4.2.2 on 2023-09-30 08:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_alter_article_date_added_alter_article_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 30, 11, 37, 36, 119787), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='article',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 30, 11, 37, 36, 119803), verbose_name='дата редактирования'),
        ),
    ]
