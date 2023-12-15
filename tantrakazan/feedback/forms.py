from django import forms
from feedback.models import Review, Bookmark, LikeDislike
from feedback.widgets import StarRatingWidget


class ReviewForm(forms.Form):

    text = forms.CharField(label='Отзыв', widget=forms.Textarea(
                attrs={'class': 'form__input form__input--textarea', 'placeholder': 'Оставьте отзыв'}))
    review_for = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    score = forms.IntegerField(label='Оценка', required=True, widget=StarRatingWidget())


class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeDislike
        fields = ['like_or_dislike', 'content_type', 'object_id']
        widgets = {
            'like_or_dislike': forms.RadioSelect(),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
