# Generated by Django 4.2.2 on 2023-08-19 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_therapistprofile_massage_to_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapistprofile',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Адрес'),
        ),
    ]
