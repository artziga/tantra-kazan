from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from image_cropping import ImageRatioField
from listings.models import Service


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        editable=False,
        on_delete=models.CASCADE,
        related_name='profile')
    avatar = models.ImageField(upload_to='img/avatars', verbose_name='Фото профиля', default='img/avatars/default.jpeg')

    def get_absolute_url(self):
        return reverse('users:user', kwargs={'username': self.user.username})

    def __str__(self):
        return self.user.username


class TherapistProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,

        related_name='therapist_profile')
    gender = models.BooleanField(verbose_name='Пол', null=True, choices=((True, 'Мужчина'), (False, 'Женщина')))
    birth_date = models.DateField(verbose_name='Возраст', null=True)
    height = models.PositiveSmallIntegerField(verbose_name='Рост', null=True)
    weight = models.PositiveSmallIntegerField(verbose_name='Вес', null=True)
    experience = models.PositiveSmallIntegerField(verbose_name='Опыт', null=True)
    address = models.CharField(max_length=40, verbose_name='Адрес', null=True)
    show_address = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', null=True)
    show_phone_number = models.BooleanField(default=True)
    telegram_profile = models.CharField(max_length=20, verbose_name='Телеграмм', null=True)
    show_telegram_profile = models.BooleanField(default=True)
    instagram_profile = models.CharField(max_length=20, verbose_name='Инстаграм', null=True)
    show_instagram_profile = models.BooleanField(default=True)
    description = models.TextField(verbose_name='О себе', null=True)
    services = models.ManyToManyField(Service, verbose_name='Услуги')
    is_profile_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('users:therapist', kwargs={'username': self.user.username})

    def __str__(self):
        return self.user.username

    @property
    def age(self):
        born = self.birth_date
        if not born:
            return
        today = date.today()
        try:
            birthday = born.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, month=born.month + 1, day=1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year


class Photo(models.Model):
    profile = models.ForeignKey(
        TherapistProfile,
        on_delete=models.CASCADE,
        verbose_name='Юзер',
        related_name='photos')
    image = models.ImageField(upload_to='img/', verbose_name='Фото')
    caption = models.CharField(max_length=255, verbose_name='Описание')

