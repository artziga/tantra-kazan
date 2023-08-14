from main.models import User
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from listings.forms import CreateOfferForm
from listings.models import Listing
from tantrakazan.utils import DataMixin


class OfferCreateView(DataMixin, CreateView):
    model = Listing
    form_class = CreateOfferForm
    template_name = 'listings/profile.html'
    success_url = reverse_lazy('users:therapist_profile')

    def form_valid(self, form):
        form.instance.therapist = self.request.user
        photo = self.request.FILES.get(
            'photo')
        if photo:
            form.instance.photo = self.request.FILES.get(
                'photo')
        user = User.objects.get(username=self.request.user)
        user.is_active = True
        user.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}


class OfferUpdateView(OfferCreateView, UpdateView):
    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('users:therapist', kwargs={'username': username})


def remove_offer(request, pk):
    offer = Listing.objects.get(pk=pk)
    offer.delete()
    return redirect('users:therapist_profile')


class ListingListView(DataMixin, ListView):
    model = Listing
    template_name = 'listings/listings_list.html'
    context_object_name = 'listings'
    queryset = Listing.objects.filter(is_active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}
