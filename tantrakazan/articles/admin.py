from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from articles.models import Article


# class ArticleAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorWidget())
#
#     class Meta:
#         model = Article
#         fields = '__all__'


# class ArticleAdmin(admin.ModelAdmin):
#     form = ArticleAdminForm


admin.site.register(Article)
