from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, FormView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormMixin

from listings.models import Listing
from tantrakazan import settings
from users.models import *
from users.forms import RegisterUserForm, UserProfileForm, MassageTherapistProfileForm
from tantrakazan.utils import DataMixin
from users.photo_processor import crop_face
from django.core.files import File
import os


class IndexListView(DataMixin, ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'therapists'
    queryset = User.objects.filter(therapist_profile__is_profile_active=True)[:5]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Главная')
        return dict(list(context.items()) + list(context_def.items()))


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


class UserFormCreateView(DataMixin, FormView):
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
        user = User.objects.get(username=self.request.user)
        user.first_name = form.cleaned_data.pop('first_name', None)
        user.last_name = form.cleaned_data.pop('last_name', None)
        form.cleaned_data.pop('avatar', None)
        user.save()
        photo = self.request.FILES.get('avatar')
        cropped_photo = crop_face(uploaded_image=photo)
        UserProfile.objects.create(user=user, avatar=cropped_photo)
        services = form.cleaned_data.pop('services', None)
        tp = TherapistProfile.objects.create(user=user, **form.cleaned_data)
        tp.services.set(services)
        return super().form_valid(form)


class UserFormUpdateView(UserFormCreateView):

    def get_context_data(self, *, object_list=None, **kwargs):
        initial = self.get_initial()
        form = UserProfileForm(initial=initial)
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context

    def get_initial(self):
        user = User.objects.get(username=self.request.user)
        user_data = {'first_name': user.first_name, 'last_name': user.last_name}
        av = {}
        photo = UserProfile.objects.filter(user=user).values('avatar').first()
        # photo_path = os.path.join(settings.MEDIA_ROOT, photo)
        # av['avatar'] = File(open(photo_path), 'rb')
        services = TherapistProfile.objects.get(user=user).services.values_list('pk', flat=True).all()
        profile_data = TherapistProfile.objects.filter(user=user).values(
            'gender',
            'birth_date',
            'height',
            'weight',
            'experience',
            'address',
            'show_address',
            'phone_number',
            'show_phone_number',
            'telegram_profile',
            'show_telegram_profile',
            'instagram_profile',
            'show_instagram_profile',
            'description',
            'is_profile_active'
        ).first()
        bd = profile_data['birth_date']
        if bd:
            profile_data['birth_date'] = bd.isoformat()
        profile_data['services'] = list(services)
        return user_data | photo | profile_data

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        user.first_name = form.cleaned_data.pop('first_name', None)
        user.last_name = form.cleaned_data.pop('last_name', None)
        form.cleaned_data.pop('avatar', None)
        user.save()
        photo = self.request.FILES.get('avatar')
        if photo:
            # print('центр', find_face(photo) or 'нет лица')
            cropped_photo = crop_face(uploaded_image=photo)
            up = UserProfile.objects.get(user=user)
            print(cropped_photo)
            up.avatar = cropped_photo
            up.save()
        services = form.cleaned_data.pop('services', None)
        tp = TherapistProfile.objects.get(user=user)
        for field in form.cleaned_data:
            value = form.cleaned_data[field]
            setattr(tp, field, value)
        tp.services.set(services)
        tp.save()
        return FormMixin.form_valid(self, form)


class MassageTherapistCreateView(UserFormCreateView):
    model = TherapistProfile
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
        offers = Listing.objects.filter(therapist_id=user.pk)
        return offers

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        offers = self.get_offers()
        context['offers'] = offers
        return context


class TherapistListView(DataMixin, ListView):
    model = User
    template_name = 'users/therapist_list.html'
    context_object_name = 'therapists'
    queryset = User.objects.filter(therapist_profile__is_profile_active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}
