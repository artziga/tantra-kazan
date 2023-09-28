from django import template

from gallery.models import ThumbnailsMixin

register = template.Library()


def thumbnail(image, thumbnail_type: str):
    image_url = image
    if thumbnail_type not in image.thumbnail_sizes:
        raise TypeError(f"Такой миниатюры не предусмотрено для данного изображения. Есть: {image.thumbnail_sizes}")
    path = image_url.split('/')
    filename = path[-1]
    path[-1] = f"{thumbnail_type}_{filename}"
    thumbnail_path = '/'.join(path)
    return thumbnail_path


@register.simple_tag
def generate_thumbnail_url(obj, thumbnail_type):
    if isinstance(obj, ThumbnailsMixin):
        thumbnail_name = obj.generate_thumbnail_name(thumbnail_type=thumbnail_type)
        thumbnail_path = obj.get_storage_path(filename=thumbnail_name, image_field=obj.image)
        return f'/{thumbnail_path}'
    return ''
