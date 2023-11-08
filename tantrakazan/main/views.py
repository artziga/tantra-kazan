from django.contrib.contenttypes.models import ContentType

from listings.models import Listing
from main.forms import ContactUsForm
from main.models import User

from django.db.models import Q
from django.views.generic import ListView, TemplateView, FormView

from tantrakazan.utils import DataMixin


class IndexListView(DataMixin, ListView):
    model = User
    template_name = 'main/index.html'
    context_object_name = 'therapists'
    queryset = User.objects.filter(therapist_profile__is_profile_active=True)[:5]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Главная')
        content_type = ContentType.objects.get_for_model(self.request.user)
        context['content_type_id'] = content_type.pk
        return dict(list(context.items()) + list(context_def.items()))


class SearchView(DataMixin, TemplateView):
    template_name = 'main/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Результаты поиска')
        context['relevant_therapists'] = self.get_users()
        context['relevant_listings'] = self.get_listings()
        return dict(list(context.items()) + list(context_def.items()))

    def get_users(self):
        key = self.request.GET['search']
        therapists = User.objects.filter(is_therapist=True)
        relevant_therapists = therapists.filter(
            Q(username__icontains=key) |
            Q(first_name__icontains=key) |
            Q(last_name__icontains=key)
        )
        return relevant_therapists

    def get_listings(self):
        key = self.request.GET['search']
        relevant_listings = Listing.objects.filter(
            Q(title__icontains=key)
        )
        return relevant_listings


class ContactUsView(FormView):
    template_name = 'main/contact-us.html'
    form_class = ContactUsForm
