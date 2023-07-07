from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from listings.forms import CreateOfferForm
from listings.models import Offer
from tantrakazan.utils import DataMixin


class OfferCreateView(DataMixin, CreateView):
    model = Offer
    form_class = CreateOfferForm
    template_name = 'listings/profile.html'

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

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('users:therapist', kwargs={'username': username})


class OfferUpdateView(OfferCreateView, UpdateView):
    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('users:therapist', kwargs={'username': username})


def remove_offer(request, pk):
    user = request.user
    offer = Offer.objects.get(pk=pk)
    offer.delete()
    return redirect('users:therapist', username=user.username)
