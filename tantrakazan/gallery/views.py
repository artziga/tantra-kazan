from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import FormView, CreateView, DetailView
from gallery.forms import CreateGalleryForm, AddPhotoForm
from tantrakazan.utils import DataMixin
from gallery.models import Gallery, Photo
from datetime import datetime
from unidecode import unidecode


class CreateGalleryView(DataMixin, FormView):
    form_class = CreateGalleryForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:therapist_profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Добавление альбома')
        return context | context_def

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.cleaned_data['user'] = self.request.user
        form.cleaned_data.pop('add_photos')
        gallery = Gallery.objects.create(**form.cleaned_data)
        photos = self.request.FILES.getlist('add_photos')
        if photos:
            current_gallery_photos = AddPhotosView.append_photos(photos, gallery)
            gallery.photos.add(*current_gallery_photos)
        return super().form_valid(form)


class AddPhotosView(DataMixin, FormView):
    form_class = AddPhotoForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:therapist_profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Загрузка фото')
        return context | context_def

    @staticmethod
    def append_photos(photos: list, gallery) -> list:
        current_gallery_photos = []
        for photo in photos:
            title = AddPhotosView.get_unique_name(photo.name)
            photo = Photo.objects.create(image=photo, gallery=gallery, title=title)
            current_gallery_photos.append(photo)
        return current_gallery_photos

    @staticmethod
    def get_unique_name(full_name: str) -> str:
        file_name, ert = full_name.split('.')
        now = str(datetime.now().time())
        now = now.replace('.', '').replace(':', '')
        int_now = int(now)
        hex_now = str(hex(int_now))
        unique_file_name = f'{file_name}_{hex_now[6:]}.{ert}'
        return unique_file_name


class GalleryDetailView(DataMixin, DetailView):
    template_name = 'users/therapist_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Альбом')
        return context | context_def
