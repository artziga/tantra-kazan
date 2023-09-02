from django.contrib import admin
from .models import *


class CommentAdmin(admin.ModelAdmin):
    list_display = '__all__'


admin.site.register(Comment)

