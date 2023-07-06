from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import *
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Имя пользователя'}))
    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'E-Mail'}))
    password1 = forms.CharField(label='Пароль', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='АВАТАР', required=False)
    gender = forms.NullBooleanField(required=False, label='', widget=forms.Select(
        choices=((None, 'Не выбрано'), (True, 'Мужчина'), (False, 'Женщина'))))
    age = forms.IntegerField(required=False, label='', widget=forms.NumberInput(attrs={'placeholder': 'Возраст'}))
    height = forms.IntegerField(required=False, label='', widget=forms.NumberInput(attrs={'placeholder': 'Рост'}))
    weight = forms.IntegerField(required=False, label='', widget=forms.NumberInput(attrs={'placeholder': 'Вес'}))

    class Meta:
        model = UserProfile
        fields = ('avatar', 'gender', 'age', 'height', 'weight')


class MassageTherapistProfileForm(forms.ModelForm):
    class Meta:
        model = MassageTherapistProfile
        fields = '__all__'


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'class': 'form-input'}))


class CreateOfferForm(forms.ModelForm):
    photo = forms.ImageField(label='АВАТАР', required=False)

    class Meta:
        model = Offer
        fields = '__all__'
