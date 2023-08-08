import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, FormView, TemplateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic.edit import FormMixin
from django.core.signing import BadSignature
import logging

from listings.models import Listing
from tantrakazan import settings
from users.apps import user_registered
from users.models import *
from users.forms import RegisterUserForm, UserProfileForm, MassageTherapistProfileForm, UserAvatarForm, LoginUserForm
from tantrakazan.utils import DataMixin
from users.utils import signer
from users.photo_processor import crop_face
from gallery.models import Gallery


class RegisterUserCreateView(DataMixin, CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:registration_done')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(context_def.items()))

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user_registered.send(sender=self.__class__, instance=user)
        return response


class RegisterTherapistCreateView(RegisterUserCreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        TherapistProfile.objects.create(user=user)
        return response


class RegisterDone(DataMixin, TemplateView):
    template_name = 'users/register_done.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Регистрация')
        return {**context, **context_def}


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'users/bad_signature.html')

    user = get_object_or_404(User, username=username)
    if user.is_active:
        template = 'users/user_is_activated.html'
        return render(request, template)

    user.is_active = True
    user.save()
    login(request, user)
    return redirect('users:profile')




class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('main:home')
    success_message = 'Пароль изменен'


class LoginUserView(DataMixin, LoginView):
    template_name = 'users/register.html'
    # form_class = LoginUserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Вход')
        return dict(list(context.items()) + list(context_def.items()))

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            direction = 'users:therapist'
        else:
            direction = 'users:user'
        return reverse_lazy(direction, kwargs={'username': user.username})


class AddAvatar(LoginRequiredMixin, DataMixin, FormView):
    model = User
    form_class = UserAvatarForm
    template_name = 'users/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Добавление фото пользователя')
        return dict(list(context.items()) + list(context_def.items()))

    def get_success_url(self):
        if TherapistProfile.objects.filrer(user=self.request.user).exists():
            return reverse_lazy('users:create_therapist_profile')
        return reverse_lazy('users:user', kwargs={'username': self.request.user})

    def form_valid(self, form):
        user = self.request.user
        form.cleaned_data['user'] = user
        photo = self.request.FILES.get('avatar')
        cropped_photo = crop_face(uploaded_image=photo)
        user.avatar = cropped_photo
        return super().form_valid(form)


class AddUserAvatar(AddAvatar):

    def get_success_url(self):
        return reverse_lazy('users:user', kwargs={'username': self.request.user})


class AddTherapistAvatar(AddAvatar):

    def get_success_url(self):
        return reverse_lazy('users:create_therapist_profile')


class UserFormCreateView(LoginRequiredMixin, DataMixin, FormView):
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Анкета')
        return dict(list(context.items()) + list(context_def.items()))

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('users:therapist', kwargs={'username': username})

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        user.first_name = form.cleaned_data.pop('first_name', None)
        user.last_name = form.cleaned_data.pop('last_name', None)
        form.cleaned_data.pop('avatar', None)
        user.save()
        services = form.cleaned_data.pop('services', None)
        tp = TherapistProfile.objects.create(user=user, **form.cleaned_data)
        tp.services.set(services)
        self.create_license_gallery()
        return super().form_valid(form)

    def create_license_gallery(self):
        """Для всех пользователей создающих профиль массажиста создается
        галерея сертификатов"""
        user = User.objects.get(username=self.request.user)
        license_gallery = Gallery.objects.create(user=user,
                                                 slug=f'{user.username}s_licenses',
                                                 title='Сертификаты',
                                                 description='Мои сертификаты')


class UserFormUpdateView(UserFormCreateView):

    def get_context_data(self, *, object_list=None, **kwargs):
        initial = self.get_initial()
        form = UserProfileForm(initial=initial)
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context

    def get_initial(self):
        user = self.request.user
        user_data = {'first_name': user.first_name, 'last_name': user.last_name}
        av = {}
        photo = user.avatar
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
            user.avatar = cropped_photo
            user.save()
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


class ProfileView(LoginRequiredMixin, DataMixin, TemplateView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_profile_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}


class TherapistProfileDetailView(ProfileView):
    template_name = 'users/therapist_profile_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        offers = Listing.objects.filter(therapist_id=user.pk)
        galleries = Gallery.objects.filter(user=user)
        samples = {gallery.title: gallery.sample(user=user, count=5) for gallery in galleries}
        context['offers'] = offers
        context['galleries'] = galleries
        context['samples'] = samples

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
