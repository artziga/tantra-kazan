from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from feedback.forms import CommentForm
from feedback.models import Comment
from main.models import User


class AddCommentView(View):
    def post(self, request, from_user, parent_comment_id=None):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            from_user_obj = User.objects.get(username=from_user)
            object_id = form.cleaned_data['object_id']
            content_type_id = form['content_type'].value()
            content_type = ContentType.objects.get_for_id(content_type_id)
            comment = form.save(commit=False)
            comment.author = from_user_obj
            comment.parent_id = parent_comment_id
            comment.content_type = content_type
            comment.object_id = object_id
            comment.save()
        return redirect(request.META.get('HTTP_REFERER'))


class DeleteCommentView(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('users:therapist_profile')
