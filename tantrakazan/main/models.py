from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    avatar = models.ImageField(upload_to='img/avatars', verbose_name='Фото профиля', null=True, blank=True)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates hello whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
