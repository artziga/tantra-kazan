from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from unidecode import unidecode
from multiupload.fields import MultiImageField
from django.core.validators import validate_image_file_extension
from gallery.models import Gallery, Photo


def validate_image_files_extension(value):
    for file in value:
        extension = Path(file.name).suffix[1:].lower()
        if extension not in ['jpg', 'jpeg', 'png', 'gif']:
            raise ValidationError('Допустимы только файлы с расширениями jpg, jpeg, png и gif.')


class MultiImageUploadForm(forms.ModelForm):
    image = MultiImageField(
        min_num=1,
        max_num=10,
        max_file_size=1024 * 1024 * 5,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_photo_validators = self.fields['image'].validators
        add_photo_validators.remove(validate_image_file_extension)
        add_photo_validators.append(validate_image_files_extension)


class CreateGalleryForm(MultiImageUploadForm):
    class Meta:
        model = Gallery
        fields = ['title', 'description', 'is_public']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title:
            slug = slugify(unidecode(title))
            cleaned_data['slug'] = slug
            self.instance.slug = slug
        return cleaned_data


class AddPhotoForm(MultiImageUploadForm):
    class Meta:
        model = Photo
        fields = ['image']
