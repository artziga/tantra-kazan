from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        editable=False,
        on_delete=models.CASCADE,
        related_name='profile')
    avatar = models.ImageField(upload_to='img/avatars', verbose_name='Фото профиля', default='img/avatars/default.jpeg')
    gender = models.BooleanField(verbose_name='Пол', null=True, choices=((True, 'Мужчина'), (False, 'Женщина')))
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', null=True)
    height = models.PositiveSmallIntegerField(verbose_name='Рост', null=True)
    weight = models.PositiveSmallIntegerField(verbose_name='Вес', null=True)

    def get_absolute_url(self):
        return reverse('users:user', kwargs={'username': self.user.username})

    def __str__(self):
        return self.user.username


class MassageTherapistProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        editable=False,
        related_name='massage_therapist_profile')
    experience = models.PositiveSmallIntegerField(verbose_name='Опыт', null=True)
    address = models.CharField(max_length=40, verbose_name='Адрес', null=True)
    contact_number = models.CharField(max_length=20, verbose_name='Номер телефона', null=True)
    telegram_profile = models.CharField(max_length=20, verbose_name='Телеграмм', null=True)
    instagram_profile = models.CharField(max_length=20, verbose_name='Инстаграм', null=True)
    description = models.TextField(verbose_name='О себе', null=True)

    def get_absolute_url(self):
        return reverse('users:therapist', kwargs={'username': self.user.name})

    def __str__(self):
        return self.user.name


class Photo(models.Model):
    profile = models.ForeignKey(
        MassageTherapistProfile,
        on_delete=models.CASCADE,
        verbose_name='Юзер',
        related_name='photos')
    image = models.ImageField(upload_to='img/', verbose_name='Фото')
    caption = models.CharField(max_length=255, verbose_name='Описание')


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название услуги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Offer(models.Model):
    therapist = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, verbose_name='Массажист')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга', related_name='service')
    photo = models.ImageField(upload_to='img/offers', verbose_name='Фото профиля', default='img/offers/default.jpeg')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.PositiveSmallIntegerField(verbose_name='Цена')
