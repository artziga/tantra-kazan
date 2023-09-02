from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from star_ratings.models import Rating


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
    ratings = GenericRelation(Rating, related_query_name='therapists')


    objects = UserManager()
