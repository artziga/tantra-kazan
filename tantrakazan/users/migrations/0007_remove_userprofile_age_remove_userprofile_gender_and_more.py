# Generated by Django 4.2.2 on 2023-07-08 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_alter_massagetherapistprofile_user_delete_offer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='age',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='height',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='weight',
        ),
        migrations.AddField(
            model_name='massagetherapistprofile',
            name='age',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Возраст'),
        ),
        migrations.AddField(
            model_name='massagetherapistprofile',
            name='gender',
            field=models.BooleanField(choices=[(True, 'Мужчина'), (False, 'Женщина')], null=True, verbose_name='Пол'),
        ),
        migrations.AddField(
            model_name='massagetherapistprofile',
            name='height',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Рост'),
        ),
        migrations.AddField(
            model_name='massagetherapistprofile',
            name='is_profile_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='massagetherapistprofile',
            name='weight',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Вес'),
        ),
        migrations.AlterField(
            model_name='massagetherapistprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='therapist_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
