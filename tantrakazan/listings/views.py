from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView


from listings.forms import CreateOfferForm
from listings.models import Listing
from config.utils import DataMixin

User = get_user_model()


class OfferCreateView(DataMixin, CreateView):
    model = Listing
    form_class = CreateOfferForm
    template_name = 'listings/listing_form.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.specialist = self.request.user
        listing.duration = form.cleaned_data['duration']
        listing.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}


class OfferUpdateView(OfferCreateView, UpdateView):

    def get_initial(self):
        initial = super().get_initial()
        listing = self.get_object()
        duration = listing.duration
        initial['hours'] = duration.days * 24 + duration.seconds // 3600
        initial['minutes'] = (duration.seconds // 60) % 60
        return initial


def remove_offer(request, pk):
    offer = Listing.objects.get(pk=pk)
    offer.delete()
    return redirect('users:profile')


class ListingListView(DataMixin, ListView):
    model = Listing
    template_name = 'listings/listings_list.html'
    context_object_name = 'listings'
    queryset = Listing.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}
