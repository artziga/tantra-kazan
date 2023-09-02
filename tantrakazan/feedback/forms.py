from django import forms
from feedback.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'content_type', 'object_id']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите комментарий'}),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
