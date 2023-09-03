from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from star_ratings.models import Rating

from feedback.models import Comment, Bookmark
from main.managers import CustomUserManager


class User(AbstractUser):
    avatar = models.ImageField(upload_to='img/avatars', verbose_name='Фото профиля', null=True, blank=True)
    is_active = models.BooleanField(
        "активен",
        default=False,
        help_text=_(
            "Designates hello whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_activated = models.BooleanField(verbose_name='активирован', default=False)
    is_therapist = models.BooleanField(verbose_name='Массажист', default=False)
    ratings = GenericRelation(Rating, related_name='ratings')
    bookmarks = GenericRelation(Bookmark, related_name='bookmarks')
    comments = GenericRelation(Comment, related_name='comments')

    objects = CustomUserManager()
