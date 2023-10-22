# Generated by Django 4.2.2 on 2023-10-21 06:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_therapistprofile_basic_services_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('listings', '0014_remove_basicservice_home_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicservice',
            name='home_price',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Приём у себя'),
        ),
        migrations.AddField(
            model_name='basicservice',
            name='on_site_price',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Выезд на дом'),
        ),
        migrations.AddField(
            model_name='basicservice',
            name='specialist',
            field=models.ManyToManyField(related_name='basic', to=settings.AUTH_USER_MODEL, verbose_name='Специалист'),
        ),
        migrations.DeleteModel(
            name='BasicServicePrice',
        ),
    ]