from datetime import timedelta

import arrow
from django.contrib.auth import get_user_model

from taggit.models import Tag

from django.db import models

from taggit.managers import TaggableManager

User = get_user_model()


class BasicService(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Базовая услуга'
        verbose_name_plural = 'Базовые услуги'


class BasicServicePrice(models.Model):
    service = models.ForeignKey(BasicService,
                                on_delete=models.CASCADE,
                                )
    specialist = models.ForeignKey('specialists.SpecialistProfile', on_delete=models.CASCADE, null=True)
    home_price = models.PositiveSmallIntegerField(verbose_name='Приём у себя', null=True)
    on_site_price = models.PositiveSmallIntegerField(verbose_name='Выезд на дом', null=True)


class MassageFor(models.Model):
    massage_for = models.CharField(max_length=50, verbose_name='Массаж для')
    slug = models.SlugField()
    icon = models.CharField(max_length=50, verbose_name='Иконка')

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Для кого массаж'
        verbose_name_plural = verbose_name


class Listing(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='listings',
                             related_query_name='listing',
                             verbose_name='Массажист')
    title = models.CharField(max_length=50, verbose_name='Название')
    tags = TaggableManager()
    description = models.TextField(verbose_name='Описание', null=True)
    duration = models.DurationField(verbose_name='Продолжительность')
    price = models.PositiveSmallIntegerField(verbose_name='Цена')

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'

    def __str__(self):
        return self.title


class Feature(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
