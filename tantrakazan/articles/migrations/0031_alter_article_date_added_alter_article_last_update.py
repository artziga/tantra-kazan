# Generated by Django 4.2.2 on 2023-10-26 18:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0030_alter_article_date_added_alter_article_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 26, 21, 18, 48, 717940), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='article',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 26, 21, 18, 48, 717956), verbose_name='дата редактирования'),
        ),
    ]
