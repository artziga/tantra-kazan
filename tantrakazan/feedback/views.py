import json

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from feedback.forms import CommentForm, LikeForm
from feedback.models import Comment, LikeDislike, Bookmark
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
        return reverse_lazy('users:profile')


class BookmarkView(LoginRequiredMixin, View):

    def post(self, request, obj_pk, content_type_id):
        # нам потребуется пользователь
        user = auth.get_user(request)
        content_type = ContentType.objects.get_for_id(content_type_id)
        # пытаемся получить закладку из таблицы, или создать новую
        bookmark, created = Bookmark.objects.get_or_create(user=user, object_id=obj_pk, content_type=content_type)
        # если не была создана новая закладка,
        # то считаем, что запрос был на удаление закладки
        if not created:
            bookmark.delete()

        return HttpResponse(
            json.dumps({
                "result": created,
                "count": Bookmark.objects.filter(object_id=obj_pk).count()
            }),
            content_type="application/json"
        )


class PutLikeView(View):
    def post(self, request, from_user):
        form = LikeForm(self.request.POST)
        if form.is_valid():
            if form.is_valid():
                from_user_obj = User.objects.get(username=from_user)
                object_id = form.cleaned_data['object_id']
                content_type_id = form.cleaned_data['content_type'].id
                like_or_dislike = form.cleaned_data['like_or_dislike']
                defaults = {
                    'user': from_user_obj,
                    'object_id': object_id,
                    'content_type_id': content_type_id,
                    'like_or_dislike': like_or_dislike
                }
                like, created = LikeDislike.objects.update_or_create(
                    defaults=defaults,
                    user=from_user_obj,
                    object_id=object_id,
                    content_type_id=content_type_id
                )

        return redirect(request.META.get('HTTP_REFERER'))
