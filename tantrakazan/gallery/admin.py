from django.contrib import admin
from gallery.models import Photo
from imagekit.admin import AdminThumbnail


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slug', 'admin_thumbnail',)
    admin_thumbnail = AdminThumbnail(image_field='admin_thumbnail')


admin.site.register(Photo, PhotoAdmin)
