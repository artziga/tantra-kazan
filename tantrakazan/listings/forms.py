from django import forms

from listings.models import Offer


class CreateOfferForm(forms.ModelForm):
    photo = forms.ImageField(label='Фото', required=False)

    class Meta:
        model = Offer
        fields = '__all__'
