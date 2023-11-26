from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy

from listings.models import Listing
from main.forms import ContactUsForm
from main.models import User

from django.db.models import Q
from django.views.generic import ListView, TemplateView, FormView

from tantrakazan.settings import DEFAULT_FROM_EMAIL
from tantrakazan.utils import DataMixin


def index(request):
    return render(request, 'main/index.html')


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
    template_name = 'forms/simple_form.html'
    form_class = ContactUsForm
    extra_context = {
        'button_label': 'Отправить',
        'title': 'Обратная связь'
                     }
    success_url = reverse_lazy('specialists:specialistsmi')

    def form_valid(self, form):
        subject = 'Новое обращение'
        message = (f'Оращение от {form.cleaned_data.get("name", "неизвестного")}:'
                   f' \n{form.cleaned_data.get("text", "без текста")}'
                   f'\n{form.cleaned_data.get("name", "неизвестный")} '
                   f'ожидает ответ на электронную почту по адресу {form.cleaned_data.get("email", "???")}')
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = ['kazan-tantra@yandex.ru']

        send_mail(subject, message, from_email, recipient_list)  # TODO: Надо сделать асинхронно
        return super().form_valid(form)
