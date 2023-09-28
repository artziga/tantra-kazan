from django.contrib import admin
from gallery.models import Gallery, Photo
from imagekit.admin import AdminThumbnail


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'gallery', 'slug', 'title', 'admin_thumbnail',)
    admin_thumbnail = AdminThumbnail(image_field='admin_thumbnail')


admin.site.register(Photo, PhotoAdmin)

admin.site.register(Gallery)
