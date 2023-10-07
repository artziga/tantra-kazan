# Generated by Django 4.2.2 on 2023-09-30 12:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_alter_article_date_added_alter_article_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 30, 15, 56, 6, 556426), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='article',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 30, 15, 56, 6, 556443), verbose_name='дата редактирования'),
        ),
    ]
