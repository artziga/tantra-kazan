import logging

from ckeditor.widgets import CKEditorWidget
from django import forms

from users.models import *


class CreateAvatarForm(forms.Form):
    avatar = forms.ImageField(label='АВАТАР', required=False, widget=forms.ClearableFileInput())

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data.pop('avatar', None)
        return cleaned_data


class PersonDataForm(forms.Form):
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Фамилия'}))
    gender = forms.NullBooleanField(label='', widget=forms.Select(
        choices=((None, 'Укажите свой пол'), (True, 'Мужчина'), (False, 'Женщина'))))
    birth_date = forms.DateField(label='Дата рождения', required=False,
                                 widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Дата рождения'}))
    height = forms.IntegerField(required=False, label='', widget=forms.NumberInput(attrs={'placeholder': 'Рост'}))
    weight = forms.IntegerField(required=False, label='', widget=forms.NumberInput(attrs={'placeholder': 'Вес'}))


class TherapistDataForm(forms.Form):
    massage_to_male_or_female = forms.NullBooleanField(required=False, label='Кому делаете массаж?',
                                                       widget=forms.Select(
                                                           choices=((None, 'Всем'),
                                                                    (True, 'Мужчинам'),
                                                                    (False, 'Женщинам'))))
    experience = forms.IntegerField(required=False, label='Опыт',
                                    widget=forms.NumberInput(attrs={'placeholder': 'Опыт'}))

    def clean(self):
        cleaned_data = super().clean()
        massage_to_male_or_female = cleaned_data.pop('massage_to_male_or_female')
        if massage_to_male_or_female is True:
            cleaned_data['massage_to_female'] = False
            cleaned_data['massage_to_male'] = True
        elif massage_to_male_or_female is False:
            cleaned_data['massage_to_male'] = False
            cleaned_data['massage_to_female'] = True
        else:
            cleaned_data['massage_to_male'] = True
            cleaned_data['massage_to_female'] = True
        logging.info(f'cleaned data {cleaned_data}')
        return cleaned_data


class AboutForm(forms.Form):
    description = forms.CharField(required=False, label='О себе', widget=CKEditorWidget(
        attrs={'class': 'form-input', 'placeholder': 'О себе'}))


class ContactDataForm(forms.Form):
    address = forms.CharField(required=False, label='Адрес', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Адрес: Улица, д. ХХ', 'id': 'addressInput'}))
    phone_number = forms.CharField(required=False, label='Телефон', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Телефон'}))
    telegram_profile = forms.CharField(required=False, label='Телеграм', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Телеграм'}))
    instagram_profile = forms.CharField(required=False, label='Инстаграм', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Инстаграм'}))

    def clean(self):
        cleaned_data = super().clean()
        address = cleaned_data['address']
        if address:
            raw_address = 'Казань, ' + cleaned_data['address']
            place = Locator(raw_place=raw_address)
            cleaned_data['address'] = place.location
            cleaned_data['latitude'] = place.location.point.latitude
            cleaned_data['longitude'] = place.location.point.longitude
        return cleaned_data


class ActivateProfileForm(forms.Form):
    is_profile_active = forms.BooleanField(required=False)


class TherapistProfileForm(CreateAvatarForm):
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Фамилия'}))
    gender = forms.NullBooleanField(label='', widget=forms.Select(
        choices=((None, 'Укажите свой пол'), (True, 'Мужчина'), (False, 'Женщина'))))
    massage_to_male_or_female = forms.NullBooleanField(required=False, label='Кому делаете массаж?',
                                                       widget=forms.Select(
                                                           choices=((None, 'Всем'),
                                                                    (True, 'Мужчинам'),
                                                                    (False, 'Женщинам'))))
    birth_date = forms.DateField(label='Дата рождения', required=False,
                                 widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Дата рождения'}))
    height = forms.IntegerField(required=False, label='', widget=forms.NumberInput(attrs={'placeholder': 'Рост'}))
    weight = forms.IntegerField(required=False, label='', widget=forms.NumberInput(attrs={'placeholder': 'Вес'}))
    experience = forms.IntegerField(required=False, label='Опыт',
                                    widget=forms.NumberInput(attrs={'placeholder': 'Опыт'}))
    address = forms.CharField(required=False, label='Адрес', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Адрес: Улица, д. ХХ', 'id': 'addressInput'}))
    show_address = forms.BooleanField(required=False)
    phone_number = forms.CharField(required=False, label='Телефон', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Телефон'}))
    show_phone_number = forms.BooleanField(required=False, label='Показывать номер')
    telegram_profile = forms.CharField(required=False, label='Телеграм', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Телеграм'}))
    show_telegram_profile = forms.BooleanField(required=False, label='Показывать ссылку на телеграмм')
    instagram_profile = forms.CharField(required=False, label='Инстаграм', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Инстаграм'}))
    show_instagram_profile = forms.BooleanField(required=False, label='Показывать ссылку на инстаграмм')
    short_description = forms.CharField(required=False, label='О себе', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Короткое описание'}))
    description = forms.CharField(required=False, label='О себе', widget=CKEditorWidget(
        attrs={'class': 'form-input', 'placeholder': 'О себе'}))
    is_profile_active = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        massage_to_male_or_female = cleaned_data.pop('massage_to_male_or_female')
        if massage_to_male_or_female is not None:
            if massage_to_male_or_female:
                cleaned_data['massage_to_female'] = False
            else:
                cleaned_data['massage_to_male'] = False
        address = cleaned_data['address']
        if address:
            raw_address = 'Казань, ' + cleaned_data['address']
            place = Locator(raw_place=raw_address)
            cleaned_data['address'] = place.location
            cleaned_data['latitude'] = place.location.point.latitude
            cleaned_data['longitude'] = place.location.point.longitude
        return cleaned_data


class TherapistFilterForm(forms.Form):
    gender_male = forms.BooleanField(label='Мужчина', widget=forms.CheckboxInput())
    gender_female = forms.BooleanField(label='Женщина', widget=forms.CheckboxInput())
    massage_to_male = forms.BooleanField(label='Массаж мужчинам', widget=forms.CheckboxInput())
    massage_to_female = forms.BooleanField(label='Массаж женщинам', widget=forms.CheckboxInput())
    massage_to_couples = forms.BooleanField(label='Массаж парам', widget=forms.CheckboxInput())
    price_lte_3000 = forms.BooleanField(label='₽1000 - ₽3000', widget=forms.CheckboxInput())
    price_3000_7000 = forms.BooleanField(label='₽3000 - ₽7000', widget=forms.CheckboxInput())
    price_gte_7000 = forms.BooleanField(label='₽7000 - ₽20000', widget=forms.CheckboxInput())

    def get_query_params(self):
        query_params = {}
        for key, value in self.cleaned_data.items():
            if value:
                query_params[key] = value
        return query_params

    def filter(self, queryset):
        today = date.today()
        filters = {}
        gender = self.cleaned_data.get('gender')
        min_age = self.cleaned_data.get('min_age')
        max_age = self.cleaned_data.get('max_age')
        min_weight = self.cleaned_data.get('min_weight')
        max_weight = self.cleaned_data.get('max_weight')
        min_height = self.cleaned_data.get('min_height')
        max_height = self.cleaned_data.get('max_height')
        min_experience = self.cleaned_data.get('min_experience')
        massage_to_male_or_female = self.cleaned_data.get('massage_to_male_or_female', None)
        if max_age:
            filters['therapist_profile__birth_date__gte'] = today.replace(year=today.year - (max_age + 1))
        if min_age:
            filters['therapist_profile__birth_date__lte'] = today.replace(year=today.year - min_age)
        if min_weight:
            filters['therapist_profile__weight__gte'] = min_weight
        if max_weight:
            filters['therapist_profile__weight__lte'] = max_weight
        if min_height:
            filters['therapist_profile__height__gte'] = min_height
        if max_height:
            filters['therapist_profile__height__lte'] = max_height
        if min_experience:
            filters['therapist_profile__experience__gte'] = min_experience
        if massage_to_male_or_female is not None:
            if massage_to_male_or_female:
                filters['therapist_profile__massage_to_male'] = True
            else:
                filters['therapist_profile__massage_to_female'] = True
        if gender is not None:
            filters['therapist_profile__gender'] = gender
        queryset = queryset.filter(**filters).distinct()
        return queryset


ORDERINGS = (('random', 'Случайная сортировка'),
             ('ratings__average', 'Рейтинг'),
             ('-price', 'Цена ↑'),
             ('price', 'Цена ↓'),
             ('-age', 'Возраст ↑'),
             ('age', 'Возраст ↓'),
             ('experience', 'Опыт'),
             ('comments_count', 'Количество отзывов'),
             ('added', 'Сначала новые'))


class OrderingForm(forms.Form):
    order_by = forms.ChoiceField(
        label='',
        widget=forms.Select(attrs={'class': 'product-ordering__select nice-select'}),
        choices=ORDERINGS
    )
