from functools import wraps

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render


class SpecialistOnlyMixin(PermissionRequiredMixin):

    def has_permission(self):
        return self.request.user.is_authenticated and self.request.user.is_therapist

    def handle_no_permission(self):
        return render(self.request, 'accounts/403.html', status=403)


def specialist_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_therapist):
            render(request, 'accounts/403.html', status=403)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
