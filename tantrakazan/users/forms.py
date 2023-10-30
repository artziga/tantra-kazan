import datetime
import logging

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.db.models import Q

from listings.models import MassageFor
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


price_range = {'low': (1000, 3000), 'medium': (3000, 7000), 'high': (7000, 20000)}
ORDERINGS = (('?', 'Случайная сортировка'),
             ('-ratings__average', 'Рейтинг'),
             ('min_price', 'Цена ↑'),
             ('-min_price', 'Цена ↓'),
             ('-therapist_profile__birth_date', 'Возраст ↑'),
             ('therapist_profile__birth_date', 'Возраст ↓'),
             ('therapist_profile__experience', 'Опыт'),
             ('-comments_count', 'Количество отзывов'),
             ('-date_joined', 'Сначала новые'))


class TherapistFilterForm(forms.Form):
    gender = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[(True, 'Мужчина'), (False, 'Женщина')],
    )

    massage_for = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=MassageFor.objects.values_list('slug', 'massage_for')
        # TODO: так нельзя оставлять. сломается при сносе бд
    )
    price = forms.ChoiceField(required=False,
                              widget=forms.RadioSelect,
                              choices=[(key, f'₽{price_range[key][0]} - ₽{price_range[key][1]}') for key in price_range]
                              )

    order_by = forms.ChoiceField(
        required=False,
        label='',
        widget=forms.Select(attrs={'class': 'product-ordering__select nice-select'}),
        choices=ORDERINGS
    )

    def get_query_params(self):
        query_params = {}
        for key, value in self.cleaned_data.items():
            if value:
                query_params[key] = value
        return query_params

    def filter(self, queryset):
        genders = self.cleaned_data.get('gender') or [True, False]
        massage_for = self.cleaned_data.get('massage_for') or ['for_males', 'for_females', 'for_pairs']
        price = self.cleaned_data.get('price')
        queryset = (queryset.
                    filter(
            therapist_profile__gender__in=genders,
            therapist_profile__massage_for__slug__in=massage_for
        )
                    .distinct())
        if price:
            price_filter = Q(min_price__gte=price_range[price][0], min_price__lte=price_range[price][1])
            queryset = queryset.filter(price_filter)
        ordering = self.cleaned_data.get('order_by')

        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset


class FeaturesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        features = Feature.objects.values_list('id', 'name')
        for massage_for_id, massage_for_name in features:
            field_name = f'feature_{massage_for_id}'
            self.fields[field_name] = forms.BooleanField(
                required=False,
                label=massage_for_name,
                widget=forms.CheckboxInput()
            )


class OrderingForm(forms.Form):
    order_by = forms.ChoiceField(
        label='',
        widget=forms.Select(attrs={'class': 'product-ordering__select nice-select'}),
        choices=ORDERINGS
    )
