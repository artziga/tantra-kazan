import logging
import os
import random
from io import BytesIO

from PIL import Image
from django.conf import settings
from main.models import User
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_str, filepath_to_uri, smart_str
from django.utils.safestring import mark_safe

from gallery.mangers import GalleryQuerySet, PhotoQuerySet
from django.utils.text import slugify
# from photologue import models as ph_models
from sortedm2m.fields import SortedManyToManyField
from unidecode import unidecode
from datetime import datetime

LATEST_LIMIT = getattr(settings, 'PHOTOLOGUE_GALLERY_LATEST_LIMIT', None)
SAMPLE_SIZE = getattr(settings, 'PHOTOLOGUE_GALLERY_LATEST_LIMIT', 3)
IMAGE_FIELD_MAX_LENGTH = getattr(settings, 'PHOTOLOGUE_IMAGE_FIELD_MAX_LENGTH', 100)
#
CROP_ANCHOR_CHOICES = (
    ('top', 'Top'),
    ('right', 'Right'),
    ('bottom', 'Bottom'),
    ('left', 'Left'),
    ('center', 'Center (Default)'),
)
#
# logger = logging.getLogger('gallery.models')
#
IMAGE_DIR = 'img/albums'
IMAGE_DIR_FOR_THUMB = 'media/img/albums'


def get_storage_path(instance, filename: str) -> str:
    user = instance.gallery.user.username
    gallery = instance.gallery.slug
    return os.path.join(IMAGE_DIR, user, gallery, filename)


class ThumbnailsMixin:

    @property
    def filename(self):
        return os.path.basename(self.image.name)

    def get_storage_path(self, filename: str) -> str:
        user = self.gallery.user.username
        gallery = self.gallery.slug
        return os.path.join(IMAGE_DIR_FOR_THUMB, user, gallery, filename)

    def generate_thumbnail_name(self, thumbnail_type: str) -> str:
        return f"{thumbnail_type}_{self.slug}"

    @property
    def admin_thumbnail(self):
        thumbnail_name = self.generate_thumbnail_name('admin_thumbnail')
        return f'/{self.get_storage_path(thumbnail_name)}'

    @property
    def thumbnail(self):
        thumbnail_name = self.generate_thumbnail_name('thumbnail')
        return f'/{self.get_storage_path(thumbnail_name)}'

    def create_thumbnail(self, thumbnail_type: str) -> None:
        if self.image:
            self.image.file.seek(0)
            img_bytes = self.image.file.read()
            img = Image.open(BytesIO(img_bytes))
            img = self.crop_image_to_square(img)
            img.thumbnail(size=thumbnails[thumbnail_type])
            thumbnail_name = self.generate_thumbnail_name(thumbnail_type=thumbnail_type)
            thumbnail_path = self.get_storage_path(filename=thumbnail_name)
            os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
            img.save(thumbnail_path, 'PNG')

    @staticmethod
    def crop_image_to_square(image):
        image_width, image_height = image.size
        if image_width == image_height:
            return image
        diff = abs(image_width - image_height)
        if image_width > image_height:
            left = diff / 2
            right = image_width - diff / 2
            upper = 0
            lower = image_height
        else:
            left = 0
            right = image_width
            upper = diff / 2
            lower = image_height - diff / 2
        return image.crop((left, upper, right, lower))


thumbnails = {
    'admin_thumbnail': (100, 100),
    'thumbnail': (250, 250)
}


class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_added = models.DateTimeField('дата создания',
                                      default=datetime.now())
    title = models.CharField('название',
                             max_length=250,
                             unique=False)
    slug = models.SlugField('слаг',
                            unique=True,
                            max_length=250,
                            help_text='A "slug" is a unique URL-friendly title for an object.')
    description = models.TextField('описание',
                                   blank=True)
    is_public = models.BooleanField('отображать',
                                    default=True,
                                    help_text='Public galleries will be displayed '
                                              'in the default views.')
    objects = GalleryQuerySet

    class Meta:
        unique_together = [('user', 'slug'), ('user', 'title')]
        ordering = ['-date_added', '-pk']
        get_latest_by = 'date_added'
        verbose_name = 'альбом'
        verbose_name_plural = 'альбомы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gallery:gallery', args=[self.slug])

    def latest(self, limit=LATEST_LIMIT, public=True):
        if not limit:
            limit = self.photo_count()
        if public:
            return self.public()[:limit]
        else:
            return self.photos.photo_count()[:limit]

    def sample(self, count=None):
        """Return a sample of photos, ordered at random.
        If the 'count' is not specified, it will return a number of photos
        limited by the GALLERY_SAMPLE_SIZE setting.
        """
        if count:
            if count > self.photo_count():
                count = self.photo_count()
        else:
            count = SAMPLE_SIZE
        photo_set = self.photos.all()
        return random.sample(set(photo_set), count)

    def photo_count(self, public=True):
        """Return a count of all the photos in this gallery."""
        return self.photos.count()

    photo_count.short_description = 'количество'


class Photo(ThumbnailsMixin, models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    slug = models.SlugField('слаг',
                            unique=True,
                            max_length=250,
                            help_text='A "slug" is a unique URL-friendly title for an object.')
    gallery = models.ForeignKey(Gallery,
                                on_delete=models.CASCADE,
                                verbose_name='альбом',
                                related_query_name='photos',
                                related_name='photos')
    description = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(verbose_name='фото',
                              max_length=IMAGE_FIELD_MAX_LENGTH,
                              upload_to=get_storage_path)
    upload_date = models.DateTimeField('дата загрузки',
                                       default=datetime.now())

    def next(self):
        photo_gallery = self.__class__.objects.filter(gallery=self.gallery)
        next_photo = photo_gallery.filter(pk__gt=self.pk).order_by('pk').first()
        if not next_photo:
            next_photo = photo_gallery.last()
        return next_photo

    def prev(self):
        photo_gallery = self.__class__.objects.filter(gallery=self.gallery)
        prev_photo = photo_gallery.filter(pk__lt=self.pk).order_by('-pk').first()
        if not prev_photo:
            prev_photo = photo_gallery.first()
        return prev_photo

    def save(self, *args, **kwargs):
        if self.image:
            filename, _ = os.path.splitext(self.title)
            self.slug = slugify(unidecode(filename))
            for thumbnail in thumbnails:
                self.create_thumbnail(thumbnail_type=thumbnail)
        super().save()

    def delete(self, *args, **kwargs):
        for thumbnail_type in thumbnails:
            thumbnail_path = self.generate_thumbnail_name(thumbnail_type)
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-created_at', '-pk']
        get_latest_by = 'created_at'
        verbose_name = 'фото'
