# Generated by Django 4.2.2 on 2023-07-13 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('listings', '0003_listing_is_active_alter_listing_therapist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='photo',
            field=models.ImageField(default='img/offers/default.jpg', null=True, upload_to='img/offers', verbose_name='Фото карточки'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing', related_query_name='listings', to=settings.AUTH_USER_MODEL, verbose_name='Массажист'),
        ),
    ]