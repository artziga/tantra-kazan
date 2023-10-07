# Generated by Django 4.2.2 on 2023-09-11 18:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_article_tags_alter_article_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 11, 21, 21, 56, 193749), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='article',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 11, 21, 21, 56, 193765), verbose_name='дата редактирования'),
        ),
    ]