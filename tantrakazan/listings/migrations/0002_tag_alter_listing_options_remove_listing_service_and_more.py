# Generated by Django 4.2.2 on 2023-08-16 18:35

from django.db import migrations, models
import listings.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('users', '0002_remove_therapistprofile_services_and_more'),
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=255, unique=True, verbose_name='тэг')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.AlterModelOptions(
            name='listing',
            options={'verbose_name': 'услуга', 'verbose_name_plural': 'услуги'},
        ),
        migrations.RemoveField(
            model_name='listing',
            name='service',
        ),
        migrations.AddField(
            model_name='listing',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name=listings.models.Tag),
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]
