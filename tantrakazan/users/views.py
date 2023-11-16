import os

import six
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Count, Case, Q, F, When, PositiveSmallIntegerField, OuterRef, Value, BooleanField, \
    Subquery, ExpressionWrapper
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
from accounts.views import MyPasswordChangeView
from feedback.forms import ReviewForm, LikeForm
from feedback.models import LikeDislike, Bookmark
from gallery.forms import MultiImageUploadForm, AvatarForm
from gallery.views import add_avatar
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
        context_def = self.get_user_context(title='Профиль')
        context['selected'] = self.request.user.username
        return {**context, **context_def}


class Favorite(ListView):
    context_object_name = 'favorite_specialists'
    template_name = 'users/profile_favorite.html'

    def get_queryset(self):
        ct = ContentType.objects.get_for_model(User)
        favorite_specialists_pk = (Bookmark.objects.
                                   filter(content_type=ct, user=self.request.user).values_list('object_id', flat=True))
        favorite_specialists = User.objects.filter(pk__in=favorite_specialists_pk).annotate(
            min_price=F('therapist_profile__basicserviceprice__home_price'),
            # TODO: сейчас всегда берётся цена дома, нужно сделать чтобы выбиралась наименьшая из дома/на выезде
        )
        bookmarked_subquery = Bookmark.objects.filter(
            user=self.request.user,
            content_type=ContentType.objects.get_for_model(User),
            object_id=OuterRef('pk')
        ).values('user').annotate(is_bookmarked=Value(True, output_field=BooleanField())).values('is_bookmarked')
        favorite_specialists = favorite_specialists.annotate(
            is_bookmarked=Subquery(bookmarked_subquery, output_field=BooleanField())
            )
        return favorite_specialists

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = 'Избранное'
        context['content_type_id'] = ContentType.objects.get_for_model(User).pk
        return context


class EditProfile(UpdateView):
    model = User
    template_name = 'users/profile_edit.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        add_avatar(user=self.request.user, form=form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = 'Редактировать профиль'
        return context


class UserPasswordChangeView(MyPasswordChangeView):
    template_name = 'users/profile_change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = 'Сменить пароль'
        return context
