from datetime import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from feedback.managers import LikeDislikeManager
from tantrakazan import settings


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='автор', related_query_name='comments')
    text = models.TextField(max_length=255, verbose_name='комментарий')
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='родительский комментарий',
        related_query_name='child_comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    date_added = models.DateTimeField('дата создания',
                                      default=datetime.now())
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Bookmark(models.Model):
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.user.username


class LikeDislike(Bookmark):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (LIKE, 'Нравится'),
        (DISLIKE, 'Не нравится')
    )

    like_or_dislike = models.BooleanField(default=True, verbose_name='голос',
                                          choices=VOTES)

    objects = LikeDislikeManager()
