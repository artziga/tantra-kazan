# Generated by Django 4.2.2 on 2023-10-25 18:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedback', '0041_review_delete_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=255, verbose_name='Отзыв')),
                ('rating', models.SmallIntegerField(verbose_name='Оценка')),
                ('date_added', models.DateTimeField(default=datetime.datetime(2023, 10, 25, 21, 29, 21, 776606), verbose_name='Дата создания')),
                ('object_id', models.PositiveIntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_comments', related_query_name='child_comment', to='feedback.comment', verbose_name='Родительский комментарий')),
            ],
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
