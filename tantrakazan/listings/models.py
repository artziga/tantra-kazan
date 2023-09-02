from datetime import timedelta

import arrow

from taggit.models import Tag


from main.models import User
from django.db import models

from taggit.managers import TaggableManager


class Listing(models.Model):
    therapist = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='listing',
                                  related_query_name='listings',
                                  verbose_name='Массажист')
    title = models.CharField(max_length=50, verbose_name='название')
    tags = TaggableManager()
    photo = models.ImageField(upload_to='img/offers', verbose_name='фото карточки', null=True,
                              default='img/offers/default.jpg')
    description = models.TextField(verbose_name='описание', null=True)
    duration = models.DurationField(verbose_name='продолжительность')
    price = models.PositiveSmallIntegerField(verbose_name='цена')
    is_active = models.BooleanField(default=True, verbose_name='опубликовать')

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'

    def __str__(self):
        return self.title

    @property
    def display_duration(self):
        hours = self.duration.seconds // 3600
        minutes = (self.duration.seconds // 60) % 60
        return f'{hours:02d} ч {minutes:02d} м'
