import logging
import os

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import FormView, CreateView, DetailView, UpdateView, DeleteView, ListView
from gallery.forms import AddPhotosForm
from tantrakazan.utils import DataMixin
from gallery.models import Photo
from datetime import datetime
from unidecode import unidecode


def add_avatar(form, user, get='avatar'):
    image = form.files.get(get)
    if image:
        avatar = Photo.objects.create(image=image, user=user)
        avatar.make_as_avatar()


def add_photos(form, user, get='photos'):
    photos = form.files.getlist(get)
    if photos:
        for photo in photos:
            Photo.objects.create(image=photo, user=user)


class EditGallery(DataMixin, FormView):
    form_class = AddPhotosForm
    template_name = 'gallery/gallery_form.html'
    success_url = reverse_lazy('gallery:edit_gallery')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Загрузка фото')
        specialist = self.request.user
        photos = Photo.objects.filter(user=specialist)
        context['photos'] = photos
        return context | context_def

    def form_valid(self, form):
        user = self.request.user
        add_avatar(form=form, user=user)
        add_photos(form=form, user=user)
        return super().form_valid(form)


class PhotoDeleteView(DeleteView):
    model = Photo
    success_url = reverse_lazy('specialists:profile')

    def get_success_url(self):
        return reverse_lazy('gallery:edit_gallery')


def make_photo_as_avatar(photo_id):
    photo = Photo.objects.get(pk=photo_id)
    photo.make_as_avatar()


def change_avatar(request, pk):
    try:
        current_avatar = Photo.objects.get(user=request.user, is_avatar=True)
    except ObjectDoesNotExist:
        make_photo_as_avatar(photo_id=pk)
        return redirect('gallery:edit_gallery')
    new_avatar = Photo.objects.get(pk=pk)
    context = {'current_avatar': current_avatar, 'new_avatar': new_avatar}
    return render(request, template_name='gallery/change_avatar_confirmation.html', context=context)


def change_avatar_confirm(request, pk):
    make_photo_as_avatar(photo_id=pk)
    return redirect('gallery:edit_gallery')
