from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError
from multiupload.fields import MultiImageField
from django.core.validators import validate_image_file_extension
from gallery.models import Photo


def validate_image_files_extension(value):
    for file in value:
        extension = Path(file.name).suffix[1:].lower()
        if extension not in ['jpg', 'jpeg', 'png', 'gif']:
            raise ValidationError('Допустимы только файлы с расширениями jpg, jpeg, png и gif.')


class MultiImageUploadForm(forms.Form):
    photos = MultiImageField(
        label='Фотографии',
        min_num=1,
        max_num=10,
        max_file_size=1024 * 1024 * 5,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_photo_validators = self.fields['photos'].validators
        add_photo_validators.remove(validate_image_file_extension)
        add_photo_validators.append(validate_image_files_extension)


class AddPhotosForm(MultiImageUploadForm):
    class Meta:
        model = Photo
        fields = ['photos']
