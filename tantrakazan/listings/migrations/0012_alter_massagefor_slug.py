# Generated by Django 4.2.2 on 2023-10-21 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0011_massagefor_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='massagefor',
            name='slug',
            field=models.SlugField(),
        ),
    ]
