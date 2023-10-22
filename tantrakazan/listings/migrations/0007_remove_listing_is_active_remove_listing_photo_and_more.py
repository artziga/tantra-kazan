# Generated by Django 4.2.2 on 2023-10-20 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('listings', '0006_alter_listing_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo',
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='duration',
            field=models.DurationField(verbose_name='Продолжительность'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.PositiveSmallIntegerField(verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', related_query_name='listing', to=settings.AUTH_USER_MODEL, verbose_name='Массажист'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Название'),
        ),
        migrations.CreateModel(
            name='MassageFor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('massage_for', models.CharField(max_length=50, verbose_name='Массаж для')),
                ('specialist', models.ManyToManyField(related_name='massage_for', related_query_name='massage_for', to=settings.AUTH_USER_MODEL, verbose_name='Специалист')),
            ],
            options={
                'verbose_name': 'Для кого массаж',
                'verbose_name_plural': 'Для кого массаж',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('specialist', models.ManyToManyField(related_name='features', related_query_name='feature', to=settings.AUTH_USER_MODEL, verbose_name='Специалист')),
            ],
        ),
        migrations.CreateModel(
            name='BasicServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('home_price', models.PositiveSmallIntegerField(verbose_name='Приём у себя')),
                ('on_site_price', models.PositiveSmallIntegerField(verbose_name='Выезд на дом')),
                ('specialist', models.ManyToManyField(related_name='basic', to=settings.AUTH_USER_MODEL, verbose_name='Специалист')),
            ],
            options={
                'verbose_name': 'Базовая услуга',
                'verbose_name_plural': 'Базовые услуги',
            },
        ),
    ]
