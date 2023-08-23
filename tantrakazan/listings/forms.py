from django import forms

from dal import autocomplete
from taggit.forms import TagWidget, TagField
from dal_select2_taggit.widgets import TaggitSelect2

from listings.models import Listing, Tag


class CreateOfferForm(autocomplete.FutureModelForm):
    photo = forms.ImageField(label='Фото', required=False)
    tags = TagField(
        required=False,
        widget=TagWidget(attrs={'placeholder': 'Вводите тэги через запятую'})
    )

    # def clean(self):
    #     cleaned_data = super().clean()
    #     tags = self._clean_tags()
    #     cleaned_data['tags'] = tags
    #     return cleaned_data
    #
    # def _clean_tags(self):
    #     tags_names = set(tag.strip() for tag in self.cleaned_data['tags'].split(','))
    #     tags = set()
    #     for tag_name in tags_names:
    #         tag, created = Tag.objects.get_or_create(tag_name=tag_name)
    #         tags.add(tag)
    #     return tags

    class Meta:
        model = Listing
        exclude = ['therapist']
