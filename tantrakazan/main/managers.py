from django.contrib.auth import models
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q, F


class CustomUserManager(models.UserManager):
    def active_therapists(self):
        return self.filter(
            therapist_profile__is_profile_active=True
        )

    def with_comments_count(self):
        return self.filter(therapist_profile__is_profile_active=True).annotate(
            comments_count=Count('comments')
        )
