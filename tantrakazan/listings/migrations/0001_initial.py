# Generated by Django 5.0 on 2023-12-15 09:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BasicService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Базовая услуга',
                'verbose_name_plural': 'Базовые услуги',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('duration', models.DurationField(verbose_name='Продолжительность')),
                ('price', models.PositiveSmallIntegerField(verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'услуга',
                'verbose_name_plural': 'услуги',
            },
        ),
        migrations.CreateModel(
            name='MassageFor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('massage_for', models.CharField(max_length=50, verbose_name='Массаж для')),
                ('slug', models.SlugField()),
                ('icon', models.CharField(max_length=50, verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Для кого массаж',
                'verbose_name_plural': 'Для кого массаж',
            },
        ),
        migrations.CreateModel(
            name='BasicServicePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_price', models.PositiveSmallIntegerField(null=True, verbose_name='Приём у себя')),
                ('on_site_price', models.PositiveSmallIntegerField(null=True, verbose_name='Выезд на дом')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.basicservice')),
            ],
        ),
    ]
