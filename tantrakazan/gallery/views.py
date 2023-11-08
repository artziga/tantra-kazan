import os

from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import FormView, CreateView, DetailView, UpdateView, DeleteView, ListView
from gallery.forms import AddPhotosForm
from tantrakazan.utils import DataMixin
from gallery.models import Photo
from datetime import datetime
from unidecode import unidecode


class AddPhotosView(DataMixin, FormView):
    form_class = AddPhotosForm
    template_name = 'main/form.html'
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Загрузка фото')
        return context | context_def

    def form_valid(self, form):
        # form.cleaned_data.pop('image')
        photos = self.request.FILES.getlist('photos')
        print(self.request.FILES)
        print(photos)
        for photo in photos:
            Photo.objects.create(image=photo, user=self.request.user)
        return super().form_valid(form)


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
    success_url = reverse_lazy('users:profile')

    def get_success_url(self):
        deleted_photo = self.get_object()
        gallery_slug = deleted_photo.gallery.slug
        return reverse_lazy('gallery:gallery', kwargs={'slug': gallery_slug})
