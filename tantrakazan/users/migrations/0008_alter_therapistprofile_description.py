# Generated by Django 4.2.2 on 2023-09-04 19:00

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_therapistprofile_massage_to_female_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapistprofile',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='О себе'),
        ),
    ]