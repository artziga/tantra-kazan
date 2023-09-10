from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import FormView, CreateView, DetailView, UpdateView, DeleteView, ListView
from gallery.forms import CreateGalleryForm, AddPhotoForm
from tantrakazan.utils import DataMixin
from gallery.models import Gallery, Photo
from datetime import datetime
from unidecode import unidecode


class GalleryCreateView(DataMixin, FormView):
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
        form.cleaned_data.pop('image')
        gallery = Gallery.objects.create(**form.cleaned_data)
        photos = self.request.FILES.getlist('image')
        if photos:
            current_gallery_photos = AddPhotosView.append_photos(photos, gallery)
            gallery.photos.add(*current_gallery_photos)
        return super().form_valid(form)


class GalleryUpdateView(DataMixin, UpdateView):
    model = Gallery
    template_name = 'users/profile.html'
    fields = ['title', 'description', 'is_public']
    success_url = reverse_lazy('users:therapist_profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Редактировать альбом')
        return context | context_def


class GalleryDeleteView(DeleteView):
    model = Gallery
    success_url = reverse_lazy('users:therapist_profile')


class AddPhotosView(DataMixin, FormView):
    form_class = AddPhotoForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:therapist_profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Загрузка фото')
        return context | context_def

    def form_valid(self, form):
        gallery = Gallery.objects.get(slug=self.kwargs.get('slug'))
        form.cleaned_data.pop('image')
        photos = self.request.FILES.getlist('image')
        self.append_photos(photos, gallery)
        return super().form_valid(form)

    @staticmethod
    def append_photos(photos: list, gallery) -> list:
        current_gallery_photos = []
        for photo in photos:
            title = photo.name
            photo = Photo.objects.create(image=photo, gallery=gallery, title=title)
            current_gallery_photos.append(photo)
        return current_gallery_photos


class GalleryDetailView(DataMixin, ListView):
    template_name = 'gallery/gallery.html'
    context_object_name = 'photos'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        gallery_slug = self.kwargs.get('slug')
        gallery = Gallery.objects.get(slug=gallery_slug)
        context_def = self.get_user_context(title=gallery.title, gallery=gallery)
        return context | context_def

    def get_queryset(self):
        gallery_slug = self.kwargs.get('slug')
        gallery = Gallery.objects.get(slug=gallery_slug)
        return Photo.objects.filter(gallery=gallery)


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'gallery/photo.html'
    context_object_name = 'photo'


class PhotoUpdateView(DataMixin, PhotoDetailView, UpdateView):
    fields = ['description']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Фото', edit=True)
        return context | context_def

    def get_success_url(self):
        return reverse_lazy('gallery:photo', kwargs={'slug': self.kwargs.get('slug')})


class PhotoDeleteView(DeleteView):
    model = Photo
    success_url = reverse_lazy('users:therapist_profile')

    def get_success_url(self):
        deleted_photo = self.get_object()
        gallery_slug = deleted_photo.gallery.slug
        return reverse_lazy('gallery:gallery', kwargs={'slug': gallery_slug})
