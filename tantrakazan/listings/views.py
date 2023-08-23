from main.models import User
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, FormView

from dal import autocomplete

from listings.forms import CreateOfferForm
from listings.models import Listing, Tag
from tantrakazan.utils import DataMixin


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class OfferCreateView(DataMixin, CreateView):
    model = Listing
    form_class = CreateOfferForm
    template_name = 'listings/profile.html'
    success_url = reverse_lazy('users:therapist_profile')

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.therapist = self.request.user
        self.add_listing_image(listing)
        listing.save()
        return super().form_valid(form)

    def add_listing_image(self, listing):
        photo = self.request.FILES.get('photo')
        if photo:
            listing.photo = photo

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}


class OfferUpdateView(OfferCreateView, UpdateView):
    pass


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
