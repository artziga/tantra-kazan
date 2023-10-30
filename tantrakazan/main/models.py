from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from star_ratings.models import Rating

from feedback.models import Review, Bookmark
from main.managers import CustomUserManager
from gallery.models import Avatar


class User(AbstractUser):
    avatar = models.OneToOneField(Avatar, on_delete=models.CASCADE, null=True)
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
    rating = GenericRelation(Rating, related_name='users', related_query_name='user')
    bookmarks = GenericRelation(Bookmark, related_name='bookmarks')
    reviews = GenericRelation(Review, related_name='reviews')

    objects = CustomUserManager()

    def __str__(self):
        if self.first_name or self.last_name:
            return ' '.join([self.first_name, self.last_name])
        return self.username

    @property
    def name(self):
        return self.first_name or self.username
