# Generated by Django 4.2.2 on 2023-07-08 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(null=True, upload_to='img/offers', verbose_name='Фото карточки')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('price', models.PositiveSmallIntegerField(verbose_name='Цена')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service', to='listings.service', verbose_name='Услуга')),
                ('therapist', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='listing', to=settings.AUTH_USER_MODEL, verbose_name='Массажист')),
            ],
        ),
        migrations.DeleteModel(
            name='Offer',
        ),
    ]