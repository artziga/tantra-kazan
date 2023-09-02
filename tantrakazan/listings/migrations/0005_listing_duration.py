# Generated by Django 4.2.2 on 2023-08-27 06:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_alter_listing_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(seconds=3600), verbose_name='продолжительность'),
        ),
    ]
