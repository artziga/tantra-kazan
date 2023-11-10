import json
import logging

from django.db.utils import IntegrityError
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from star_ratings.models import Rating, UserRating
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View

from feedback.forms import ReviewForm, LikeForm
from feedback.models import Review, LikeDislike, Bookmark
from main.models import User

logger = logging.getLogger(__name__)


class ReviewIntegrityError(Exception):
    pass


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request):
        form = ReviewForm(self.request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    self.create_review()
            except ReviewIntegrityError as e:
                messages.error(request, str(e))
        else:
            print(form.errors)
        return redirect(request.META.get('HTTP_REFERER'))

    def create_review(self):
        score_value = self.request.POST.get('score')
        review_for = self.request.POST.get('review_for')
        text = self.request.POST.get('text')
        specialist = User.objects.get(pk=review_for)
        ct = ContentType.objects.get_for_model(specialist)
        try:
            with transaction.atomic():
                Rating.objects.rate(instance=specialist, score=score_value, user=self.request.user)
                user_rating = UserRating.objects.get(
                    user=self.request.user,
                    rating__object_id=specialist.pk,
                    rating__content_type=ct
                )
                Review.objects.create(text=text, score=user_rating)
                logger.info(f"{self.request.user.username} оставил отзыв для {specialist}")
        except IntegrityError:
            logger.info(f"{self.request.user.username} пытался оставить второй отзыв для {specialist}")
            raise ReviewIntegrityError("Only one review allowed per user.")

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


@login_required
def delete_review(request, review_for):
    review_from = request.user
    try:
        specialist = User.objects.get(pk=review_for)
        ct = ContentType.objects.get_for_model(specialist)
        rating = Rating.objects.get(object_id=specialist.pk, content_type=ct)
        user_rating = UserRating.objects.get(user=review_from, rating=rating)
        user_rating.delete()
        logger.info(f"{request.user.username} удалил отзыв для {specialist}")
    except UserRating.DoesNotExist as e:
        logger.error(f"Ошибка удаления отзыва {request.user.username}: {e}")

    return redirect(request.META.get('HTTP_REFERER'))


class BookmarkView(LoginRequiredMixin, View):

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        obj_pk = data.get('obj_pk')
        content_type_id = data.get('content_type_id')
        user = auth.get_user(request)
        content_type = ContentType.objects.get_for_id(content_type_id)
        bookmark, created = Bookmark.objects.get_or_create(user=user, object_id=obj_pk, content_type=content_type)
        if not created:
            bookmark.delete()
        return HttpResponse(
            json.dumps({
                "result": created,
                "count": Bookmark.objects.filter(object_id=obj_pk).count()
            }),
            content_type="application/json"
        )


class PutLikeView(LoginRequiredMixin,  View):
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
