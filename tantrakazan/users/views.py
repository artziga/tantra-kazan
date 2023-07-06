from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from users.models import MassageTherapistProfile, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from users.models import *
from users.forms import RegisterUserForm, UserProfileForm, LoginUserForm, MassageTherapistProfileForm, CreateOfferForm
from users.utils import DataMixin


def index(request):
    return render(request, template_name='users/index.html')


class RegisterUserCreateView(DataMixin, CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(context_def.items()))

    def form_valid(self, form):
        response = super().form_valid(form)
        user = User.objects.get(username=self.request.user)
        user.is_active = False
        user.save()
        user = form.save()
        login(self.request, user)  # Выполнение входа пользователя
        return response


class LoginUserView(DataMixin, LoginView):
    template_name = 'users/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Вход')
        return dict(list(context.items()) + list(context_def.items()))

    def get_success_url(self):
        user = self.request.user
        print(user.is_staff)
        if user.is_staff:
            direction = 'users:therapist'
        else:
            direction = 'users:user'
        return reverse_lazy(direction, kwargs={'username': user.username})


class UserFormCreateView(DataMixin, CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Анкета')
        return dict(list(context.items()) + list(context_def.items()))

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('users:user', kwargs={'username': username})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.photo = self.request.FILES.get(
            'avatar')  # Получаем файл из request.FILES и присваиваем его полю photo объекта модели
        return super().form_valid(form)


class MassageTherapistCreateView(UserFormCreateView):
    model = MassageTherapistProfile
    form_class = MassageTherapistProfileForm

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        user.is_staff = True
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('users:therapist', kwargs={'username': username})


class UserProfileDetailView(DataMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_profile_detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}


class TherapistProfileDetailView(UserProfileDetailView):
    template_name = 'users/therapist_profile_detail.html'

    def get_offers(self):
        user = User.objects.get(username=self.request.user)
        offers = Offer.objects.filter(therapist_id=user.pk)
        return offers

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        offers = self.get_offers()
        context['offers'] = offers
        return context


class OfferCreateView(DataMixin, CreateView):
    model = Offer
    form_class = CreateOfferForm
    template_name = 'users/profile.html'

    def form_valid(self, form):
        form.instance.therapist = self.request.user
        photo = self.request.FILES.get(
            'photo')
        if photo:
            form.instance.photo = self.request.FILES.get(
                'photo')
        user = User.objects.get(username=self.request.user)
        user.is_active = True
        user.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('users:therapist', kwargs={'username': username})


def remove_offer(request, pk):
    user = request.user
    offer = Offer.objects.get(pk=pk)
    offer.delete()
    return redirect('users:therapist', username=user.username)
