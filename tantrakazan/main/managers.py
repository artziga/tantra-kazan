from django.contrib.auth import models
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q, F, Min, Case, When, PositiveSmallIntegerField



class CustomUserManager(models.UserManager):
    def active_therapists(self):
        return self.filter(
            therapist_profile__is_profile_active=True
        )


