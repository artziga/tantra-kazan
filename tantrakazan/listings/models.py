from main.models import User
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name='категория массажа')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Listing(models.Model):
    therapist = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='listing',
                                  related_query_name='listings',
                                  verbose_name='Массажист')
    title = models.CharField(max_length=50, verbose_name='название')
    service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                verbose_name='категория',
                                related_name='service',
                                help_text='можно выбрать несколько')
    photo = models.ImageField(upload_to='img/offers', verbose_name='фото карточки', null=True,
                              default='img/offers/default.jpg')
    description = models.TextField(verbose_name='описание', null=True)
    price = models.PositiveSmallIntegerField(verbose_name='цена')
    is_active = models.BooleanField(default=True, verbose_name='опубликовать')

    def __str__(self):
        return self.service.name
