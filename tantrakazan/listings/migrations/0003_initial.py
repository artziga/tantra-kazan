# Generated by Django 5.0 on 2023-12-15 09:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('listings', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='specialist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', related_query_name='listing', to=settings.AUTH_USER_MODEL, verbose_name='Массажист'),
        ),
    ]
