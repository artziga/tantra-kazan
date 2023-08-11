from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm

from main.models import User


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


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин'}))
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))

    class Meta:
        model = User
        fields = (User.USERNAME_FIELD, 'password')


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'placeholder': 'email'}),
    )
