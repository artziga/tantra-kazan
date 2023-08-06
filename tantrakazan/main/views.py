from django.contrib.auth.models import User
from django.views.generic import ListView

from tantrakazan.utils import DataMixin


class IndexListView(DataMixin, ListView):
    model = User
    template_name = 'main/index.html'
    context_object_name = 'therapists'
    queryset = User.objects.filter(therapist_profile__is_profile_active=True)[:5]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Главная')
        return dict(list(context.items()) + list(context_def.items()))
