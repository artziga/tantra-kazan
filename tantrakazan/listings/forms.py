from django import forms

from listings.models import Listing


class CreateOfferForm(forms.ModelForm):
    photo = forms.ImageField(label='Фото', required=False)

    class Meta:
        model = Listing
        exclude = ['therapist']
