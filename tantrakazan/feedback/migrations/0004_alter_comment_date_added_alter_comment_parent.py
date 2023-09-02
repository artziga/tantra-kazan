# Generated by Django 4.2.2 on 2023-08-30 08:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_comment_date_added_alter_comment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 30, 11, 33, 14, 901186), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_query_name='child_comments', to='feedback.comment', verbose_name='родительский комментарий'),
        ),
    ]