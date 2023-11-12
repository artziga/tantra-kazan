import os

import six
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Count, Case, Q, F, When, PositiveSmallIntegerField, OuterRef, Value, BooleanField, Subquery
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDict
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.views.generic import ListView, FormView, TemplateView, UpdateView
from django.db.utils import IntegrityError
from formtools.wizard.storage import NoFileStorageConfigured, BaseStorage
from formtools.wizard.views import SessionWizardView
import logging

from star_ratings.models import UserRating

from accounts.forms import MyPasswordChangeForm
from feedback.forms import ReviewForm, LikeForm
from feedback.models import LikeDislike, Bookmark
from gallery.forms import MultiImageUploadForm, AvatarForm
from listings.models import Listing
from tantrakazan import settings
from users.forms import EditProfileForm
from users.models import *
from main.models import User

from gallery.forms import AddPhotosForm as AFF
from tantrakazan.utils import DataMixin, FilterFormMixin
from gallery.photo_processor import CropFace
from gallery.models import Photo


class AddAvatar(LoginRequiredMixin, DataMixin, FormView):
    model = Photo
    form_class = AvatarForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Добавление фото пользователя')
        return dict(list(context.items()) + list(context_def.items()))

    def form_valid(self, form):
        image = self.request.FILES.get('avatar')
        if image:
            user = self.request.user
            photo, created = Photo.objects.get_or_create(is_avatar=True, user=user)
            photo.image = image
            photo.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'users/profile_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        avatar_form = AvatarForm()
        change_password_form = MyPasswordChangeForm(user=self.request.user)
        edit_form = None
        context['change_password_form'] = change_password_form
        context['avatar_form'] = avatar_form
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}

    def get_forms(self):
        avatar_form = AvatarForm()


class Favorite(ListView):
    context_object_name = 'favorite_specialists'
    template_name = 'users/profile_favorite.html'

    def get_queryset(self):
        ct = ContentType.objects.get_for_model(User)
        favorite_specialists_pk = (Bookmark.objects.
                                   filter(content_type=ct, user=self.request.user).values_list('object_id', flat=True))
        favorite_specialists = User.objects.filter(pk__in=favorite_specialists_pk)
        return favorite_specialists


class EditProfile(UpdateView):
    model = User
    template_name = 'users/profile_edit.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        avatar = form.cleaned_data.pop('avatar')
        if avatar:
            current_avatar = Photo.objects.get(user=self.request.user)
            current_avatar.image = avatar
            current_avatar.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
