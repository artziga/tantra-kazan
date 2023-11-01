import logging
import os
import random
from io import BytesIO
from datetime import datetime

from PIL import Image
from autoslug import AutoSlugField
from django.conf import settings
from django.core.files import File
from django.db.models.fields.files import FieldFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail, SmartResize, ResizeCanvas

from tantrakazan.settings import AUTH_USER_MODEL as USER
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_str, filepath_to_uri, smart_str
from django.utils.safestring import mark_safe

from gallery.mangers import GalleryQuerySet, PhotoQuerySet
from gallery.photo_processor import CropFaceProcessor, get_square_borders
from sorl.thumbnail import ImageField

from tantrakazan.settings import MEDIA_ROOT

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
    thumbnail_sizes = None
    thumbnail_fields = None

    @staticmethod
    def _filename(field: FieldFile) -> str:
        image = field
        return os.path.basename(image.name)

    def get_storage_path(self, filename: str) -> str:
        """Метод возвращает путь сохранения файла в папку для
         сохранения файла на основе параметра поля upload_to"""

        upload_to = get_storage_path(self, filename)

        return os.path.join('media/', upload_to)

    def generate_thumbnail_name(self, field: FieldFile, thumbnail_type: str) -> str:
        filename = self._filename(field)
        filename_body, ext = os.path.splitext(filename)
        if hasattr(self, 'slug') and self.slug is not None:
            return f"{thumbnail_type}_{self.slug}{ext}"
        else:
            return f"{thumbnail_type}_{filename}"

    # @property
    # def admin_thumbnail(self):
    #     thumbnail_name = self.generate_thumbnail_name('admin_thumbnail')
    #     return f'/{get_storage_path(image_field="image", filename=thumbnail_name)}'
    #
    # @property
    # def thumbnail(self):
    #     thumbnail_name = self.generate_thumbnail_name('thumbnail')
    #     return f'/{get_storage_path(image_field="image", filename=thumbnail_name)}'

    def create_thumbnail(self, field: FieldFile, thumbnail_type: str) -> None:
        image_field = field
        image_field.file.seek(0)
        img_bytes = image_field.file.read()
        img = Image.open(BytesIO(img_bytes))
        img = get_square_borders(img)
        img.thumbnail(size=self.thumbnail_sizes[thumbnail_type])
        thumbnail_name = self.generate_thumbnail_name(thumbnail_type=thumbnail_type, field=field)
        thumbnail_path = self.get_storage_path(filename=thumbnail_name)
        os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
        img.save(thumbnail_path)

    def generate_thumbnails(self):
        for field in self.thumbnail_fields:
            model_field = getattr(self, field)
            for thumbnail_type in self.thumbnail_fields[field]:
                self.create_thumbnail(field=model_field, thumbnail_type=thumbnail_type)


@receiver(post_save)
def create_thumbnails(sender, instance, **kwargs):
    if issubclass(sender, ThumbnailsMixin):
        instance.generate_thumbnails()


class Gallery(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_added = models.DateTimeField('дата создания',
                                      default=datetime.now())
    title = models.CharField('название',
                             max_length=250,
                             unique=False)
    slug = AutoSlugField(verbose_name='слаг', db_index=True, unique=True, populate_from='title')
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


class BaseImage(models.Model):
    image_size = (1000, 1000)

    def generate_slug(self):
        if self.title:
            return self.title
        elif self.image:
            image_name, ext = os.path.splitext(self.image.name)
            return image_name
        else:
            return 'no-title-and-no-image'

    title = models.CharField(max_length=100, null=True, verbose_name='название')
    slug = AutoSlugField(verbose_name='слаг', db_index=True, unique=True, populate_from=generate_slug)
    image = ProcessedImageField(verbose_name='фото',
                                processors=[ResizeToFit(*image_size)],
                                max_length=IMAGE_FIELD_MAX_LENGTH,
                                upload_to=get_storage_path,
                                )
    admin_thumbnail = ImageSpecField(source='image',
                                     processors=[Thumbnail(100, 100)
                                                 ],
                                     format='JPEG',
                                     options={'quality': 60})
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Photo(BaseImage):
    gallery = models.ForeignKey(Gallery,
                                on_delete=models.CASCADE,
                                verbose_name='альбом',
                                related_query_name='photos',
                                related_name='photos')
    description = models.CharField(max_length=150, null=True, blank=True)
    thumbnail = ImageSpecField(source='image',
                               processors=[Thumbnail(300, 300)],
                               format='JPEG',
                               options={'quality': 80})

    def save(self, *args, **kwargs):
        self.thumbnail.generate()
        self.admin_thumbnail.generate()
        return super().save()

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

    class Meta:
        ordering = ['-upload_date', '-pk']
        get_latest_by = 'upload_date'
        verbose_name = 'фото'


class Avatar(BaseImage):
    image = models.ImageField(upload_to='img/avatars', verbose_name='Фото профиля', null=True, blank=True)
    thumbnail = ImageSpecField(source='image',
                               processors=[CropFaceProcessor(margin_percent=0.6),
                                           Thumbnail(270, 300)],
                               format='JPEG',
                               options={'quality': 90})
    mini_thumbnail = ImageSpecField(source='image',
                                    processors=[CropFaceProcessor(margin_percent=0.6),
                                                Thumbnail(50, 50)],
                                    format='JPEG',
                                    options={'quality': 90})

    comment_thumbnail = ImageSpecField(source='image',
                                       processors=[CropFaceProcessor(margin_percent=0.6),
                                                   Thumbnail(100, 100)],
                                       format='JPEG',
                                       options={'quality': 90})
