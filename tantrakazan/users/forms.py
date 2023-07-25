import os

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.files import File

from tantrakazan import settings
from users.models import *
from django.contrib.auth.models import User
from listings.models import Service


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'E-Mail'}))
    password1 = forms.CharField(label='Пароль', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.Form):
    photo_path = os.path.join(settings.MEDIA_ROOT, 'img/avatars/spl-4_hh5cmZm.jpg')
    initial_avatar = File(open(photo_path, 'rb'))
    avatar = forms.ImageField(label='АВАТАР', required=False, initial=initial_avatar, widget=forms.ClearableFileInput())
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Фамилия'}))
    gender = forms.NullBooleanField(required=False, label='', widget=forms.Select(
        choices=((None, 'Не выбрано'), (True, 'Мужчина'), (False, 'Женщина'))))
    birth_date = forms.DateField(label='Дата рождения', required=False,
                                 widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Дата рождения'}))
    height = forms.IntegerField(required=False, label='', widget=forms.NumberInput(attrs={'placeholder': 'Рост'}))
    weight = forms.IntegerField(required=False, label='', widget=forms.NumberInput(attrs={'placeholder': 'Вес'}))
    experience = forms.IntegerField(required=False, label='Опыт',
                                    widget=forms.NumberInput(attrs={'placeholder': 'Опыт'}))
    address = forms.CharField(label='Адрес', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Адрес'}))
    show_address = forms.BooleanField()
    phone_number = forms.CharField(label='Телефон', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Телефон'}))
    show_phone_number = forms.BooleanField(label='Показывать номер')
    telegram_profile = forms.CharField(label='Телеграм', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Телеграм'}))
    show_telegram_profile = forms.BooleanField(label='Показывать ссылку на телеграмм')
    instagram_profile = forms.CharField(label='Инстаграм', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Инстаграм'}))
    show_instagram_profile = forms.BooleanField(label='Показывать ссылку на инстаграмм')
    description = forms.CharField(label='О себе', widget=forms.Textarea(
        attrs={'class': 'form-input', 'placeholder': 'О себе'}))
    services = forms.MultipleChoiceField(choices=Service.objects.all().values_list())
    is_profile_active = forms.BooleanField()


class MassageTherapistProfileForm(forms.ModelForm):
    class Meta:
        model = TherapistProfile
        fields = '__all__'


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'class': 'form-input'}))
