from django import forms
from feedback.models import Comment, Bookmark, LikeDislike


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'content_type', 'object_id']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите комментарий'}),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }


class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeDislike
        fields = ['like_or_dislike', 'content_type', 'object_id']
        widgets = {
            'like_or_dislike': forms.RadioSelect(),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
