from django.contrib.auth.models import User
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название услуги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Listing(models.Model):
    therapist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing', related_query_name='listings', verbose_name='Массажист')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга', related_name='service')
    photo = models.ImageField(upload_to='img/offers', verbose_name='Фото карточки', null=True, default='img/offers/default.jpg')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.PositiveSmallIntegerField(verbose_name='Цена')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.service.name

    @staticmethod
    def get_default_photo(self):
        return 'img/offers/default.jpeg'