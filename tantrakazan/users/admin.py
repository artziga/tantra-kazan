from django.contrib import admin
from .models import *


class MassageTherapistProfileAdmin(admin.ModelAdmin):
    list_display = '__all__'


# admin.site.register(UserAvatar)
admin.site.register(TherapistProfile)
