from datetime import date

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.gis.db.models import PointField
from star_ratings.models import Rating
from ckeditor.fields import RichTextField

from feedback.models import Comment
from tantrakazan.settings import AUTH_USER_MODEL as USER
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from image_cropping import ImageRatioField
from tantrakazan.utils import Locator

from gallery.models import Gallery


class TherapistProfile(models.Model):
    user = models.OneToOneField(
        USER,
        on_delete=models.CASCADE,

        related_name='therapist_profile')
    gender = models.BooleanField(verbose_name='Пол', null=True, blank=True,
                                 choices=((True, 'Мужчина'), (False, 'Женщина')))
    massage_to_male = models.BooleanField(verbose_name='массаж мужчинам', default=True, blank=True)
    massage_to_female = models.BooleanField(verbose_name='женщинам', default=True, blank=True)
    birth_date = models.DateField(verbose_name='Возраст', blank=True, null=True)
    height = models.PositiveSmallIntegerField(verbose_name='Рост', null=True, blank=True)
    weight = models.PositiveSmallIntegerField(verbose_name='Вес', null=True, blank=True)
    experience = models.PositiveSmallIntegerField(verbose_name='Опыт', null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='Адрес', null=True, blank=True)
    latitude = models.FloatField(verbose_name='широта', null=True, blank=True)
    longitude = models.FloatField(verbose_name='долгота', null=True, blank=True)
    show_address = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    show_phone_number = models.BooleanField(default=True)
    telegram_profile = models.CharField(max_length=20, verbose_name='Телеграмм', null=True, blank=True)
    show_telegram_profile = models.BooleanField(default=True)
    instagram_profile = models.CharField(max_length=20, verbose_name='Инстаграм', null=True, blank=True)
    show_instagram_profile = models.BooleanField(default=True)
    short_description = models.TextField(verbose_name='Короткое описание', null=True, blank=True)
    description = RichTextField(verbose_name='О себе', null=True, blank=True)
    is_profile_active = models.BooleanField(default=True)
    ratings = GenericRelation(Rating, related_query_name='therapists')

    @staticmethod
    def get_absolute_url():
        return reverse('users:therapist_profile')

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

    @staticmethod
    def years_suffix(years):
        last_digit = years % 10 if years > 9 else years
        if last_digit == 1:
            return 'год'
        elif last_digit in (2, 3, 4):
            return 'года'
        return 'лет'

    @property
    def display_years_suffix(self):
        if not self.age:
            return
        return self.years_suffix(self.age) or None

    @property
    def display_experience_suffix(self):
        if self.experience == 0:
            return 'года'
        if not self.experience:
            return
        return self.years_suffix(int(self.experience)) or None

    @property
    def age_display(self):
        if self.age:
            return f'{str(self.age)} {self.years_suffix(self.age)}'

    @property
    def experience_display(self):
        return f'{str(self.experience)} {self.years_suffix(int(self.experience))}'

    @property
    def gender_display(self):
        return 'Мужчина' if self.gender is True else 'Женщина'

    @property
    def point(self):
        return [self.latitude, self.longitude]
