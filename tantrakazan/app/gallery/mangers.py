from django.db.models.query import QuerySet


class SharedQueries:

    """Some queries that are identical for Gallery and Photo."""

    def is_public(self):
        """Trivial filter - will probably become more complex as time goes by!"""
        return self.filter(is_public=True)

    def for_user(self, user):
        """Return objects linked to the current user only."""
        return self.filter(user=user)


class GalleryQuerySet(SharedQueries, QuerySet):
    pass


class PhotoQuerySet(SharedQueries, QuerySet):
    pass
