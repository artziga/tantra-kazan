from django.contrib import admin
from gallery.models import Gallery, Photo


# class GalleryAdminForm(ph_admin.GalleryAdminForm):
#     class Meta(ph_admin.GalleryAdminForm.Meta):
#         model = Gallery
#
#         exclude = ['effect']
#
#
# class GalleryAdmin(ph_admin.GalleryAdmin):
#     form = GalleryAdminForm


# class PhotoAdminForm(ph_admin.PhotoAdminForm):
#     class Meta(ph_admin.PhotoAdminForm.Meta):
#         model = Photo
#         exclude = ['effect']
#
#
# class PhotoAdmin(ph_admin.PhotoAdmin):
#     form = PhotoAdminForm


admin.site.register(Gallery)
admin.site.register(Photo)
