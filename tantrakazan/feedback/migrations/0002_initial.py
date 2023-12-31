# Generated by Django 5.0 on 2023-12-15 09:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('feedback', '0001_initial'),
        ('star_ratings', '0004_alter_rating_id_alter_userrating_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='review',
            name='score',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review', related_query_name='review', to='star_ratings.userrating', verbose_name='Оценка'),
        ),
        migrations.AlterUniqueTogether(
            name='bookmark',
            unique_together={('user', 'content_type', 'object_id')},
        ),
    ]
