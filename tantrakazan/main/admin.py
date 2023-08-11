from django.contrib import admin
from main.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'is_therapist']


admin.site.register(User, UserAdmin)
