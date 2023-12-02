from ckeditor_uploader.widgets import CKEditorUploadingWidget
from dal import autocomplete
from django import forms
from taggit.forms import TagField, TagWidget
from taggit.models import Tag

from articles.models import Article


class ArticleForm(autocomplete.FutureModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    tags = TagField(
        required=False,
        widget=autocomplete.TaggitSelect2('tag_autocomplete', attrs={'placeholder': 'Вводите тэги через запятую'})
    )

    class Meta:
        model = Article
        fields = ['title', 'text', 'tags']

