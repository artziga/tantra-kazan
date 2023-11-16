from datetime import date

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.gis.db.models import PointField
from star_ratings.models import Rating
from ckeditor.fields import RichTextField

from feedback.models import Review
from listings.models import MassageFor, Feature, BasicServicePrice, BasicService
from tantrakazan.settings import AUTH_USER_MODEL as USER
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from image_cropping import ImageRatioField
from tantrakazan.utils import Locator


class TherapistProfile(models.Model):
    user = models.OneToOneField(
        USER,
        on_delete=models.CASCADE,

        related_name='therapist_profile',
        related_query_name='therapist_profile'
    )
    gender = models.BooleanField(verbose_name='Пол', null=True, blank=True,
                                 choices=((True, 'Мужчина'), (False, 'Женщина')))
    massage_for = models.ManyToManyField(MassageFor, related_name='specialists', related_query_name='specialist')
    basic_services = models.ManyToManyField(BasicService, blank=True)
    features = models.ManyToManyField(Feature, blank=True)
    birth_date = models.DateField(verbose_name='Возраст', blank=True, null=True)
    height = models.PositiveSmallIntegerField(verbose_name='Рост', null=True, blank=True)
    weight = models.PositiveSmallIntegerField(verbose_name='Вес', null=True, blank=True)
    practice_start_date = models.DateField(verbose_name='Дата начала практики', blank=True, null=True)
    address = models.CharField(max_length=200, verbose_name='Адрес', null=True, blank=True)
    latitude = models.FloatField(verbose_name='широта', null=True, blank=True)
    longitude = models.FloatField(verbose_name='долгота', null=True, blank=True)
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    telegram_profile = models.CharField(max_length=20, verbose_name='Телеграмм', null=True, blank=True)
    instagram_profile = models.CharField(max_length=20, verbose_name='Инстаграм', null=True, blank=True)
    description = models.TextField(verbose_name='О себе', null=True, blank=True)
    is_profile_active = models.BooleanField(default=True)
    rating = GenericRelation(Rating, related_query_name='therapist') #TODO: удалить перед сносом базы
    @staticmethod
    def get_absolute_url():
        return reverse('specialists:profile')

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
