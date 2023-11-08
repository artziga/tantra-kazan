import os

import six
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Count, Case, Q, F, When, PositiveSmallIntegerField, OuterRef, Value, BooleanField, Subquery
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDict
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.views.generic import ListView, FormView, TemplateView
from django.db.utils import IntegrityError
from formtools.wizard.storage import NoFileStorageConfigured, BaseStorage
from formtools.wizard.views import SessionWizardView
import logging

from star_ratings.models import UserRating

from feedback.forms import ReviewForm, LikeForm
from feedback.models import LikeDislike, Bookmark
from gallery.forms import MultiImageUploadForm
from listings.models import Listing
from tantrakazan import settings
from users.models import *
from main.models import User
from users.forms import (TherapistProfileForm,
                         AvatarForm,
                         PersonDataForm,
                         TherapistDataForm,
                         ContactDataForm,
                         AboutForm,
                         ActivateProfileForm,
                         TherapistFilterForm, AddPhotosForm,
                         )
from gallery.forms import AddPhotosForm as AFF
from tantrakazan.utils import DataMixin, FilterFormMixin
from gallery.photo_processor import CropFace
from gallery.models import Photo

FORMS = [
    ('photos', AddPhotosForm),
    ("person_data", PersonDataForm),
    ("therapist_data", TherapistDataForm),
    ("contact_data", ContactDataForm),
    ("about", AboutForm),

]
FORMS_NAMES = [

    "Общие данные",
    "Профессиональные данные",
    "Контактные данные",
    "О себе",
    "Фото",
]


def make_user_a_therapist(user):
    user.is_therapist = True
    user.save()
    TherapistProfile.objects.create(user=user)


@login_required
def become_a_therapist(request):
    return render(request, template_name='users/become_a_therapist_confirmation.html')


def become_a_therapist_confirmation(request):
    user = request.user
    make_user_a_therapist(user)
    return redirect('users:edit_profile')


class AddAvatar(LoginRequiredMixin, DataMixin, FormView):
    model = Photo
    form_class = AvatarForm
    template_name = 'users/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Добавление фото пользователя')
        return dict(list(context.items()) + list(context_def.items()))

    def get_success_url(self):
        if self.request.user.is_therapist:
            return reverse_lazy('users:edit_profile')
        return reverse_lazy('users:profile')

    def form_valid(self, form):
        photo = self.request.FILES.get('avatar')
        if photo:
            user = self.request.user
            users_avatar = Photo.objects.create(image=photo, is_avatar=True)
            user.avatar = users_avatar
            user.save()
        return super().form_valid(form)


class TherapistProfileWizard(LoginRequiredMixin, DataMixin, SessionWizardView):
    form_list = FORMS
    template_name = 'users/wizard_form.html'
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Анкета')
        context['steps'] = FORMS_NAMES
        return dict(list(context.items()) + list(context_def.items()))

    def get_form_step_files(self, form):
        if self.steps.current == 'photos':
            self.add_avatar(form)
            self.add_photos(form)
        return super().get_form_step_files(form)

    def done(self, form_list, **kwargs):
        cleaned_data = self.get_all_cleaned_data()
        user = self.request.user
        user.first_name = cleaned_data.pop('first_name', '')
        user.last_name = cleaned_data.pop('last_name', '')
        self.set_price({
            'home_price': cleaned_data.pop('home_price', ''),
            'on_site_price': cleaned_data.pop('on_site_price', '')
                        })
        massage_for_set = cleaned_data.pop('massage_for', [])
        tp, created = TherapistProfile.objects.update_or_create(user=user, defaults=cleaned_data)
        tp.massage_for.set(massage_for_set)
        user.save()
        tp.save()
        logging.info("Wizard is done")
        return redirect('users:profile')

    def add_avatar(self, form):
        avatar = form.files.get('photos-avatar')
        if avatar:
            current_avatar = Photo.objects.filter(user=self.request.user, is_avatar=True)
            if current_avatar.exists():
                current_avatar = current_avatar.first()
                current_avatar.is_avatar = False
                current_avatar.save()
            Photo.objects.create(image=avatar, user=self.request.user, is_avatar=True)

    def add_photos(self, form):
        photos = form.files.getlist('photos-photos')
        if photos:
            for photo in photos:
                Photo.objects.create(image=photo, user=self.request.user)

    def set_price(self, data):
        bs = BasicService.objects.get(pk=1)
        BasicServicePrice.objects.update_or_create(
            service=bs,
            specialist=TherapistProfile.objects.get(user=self.request.user),
            home_price=data['home_price'],
            on_site_price=data['on_site_price']
        )

    def get_form_initial(self, step):
        initial_dict = {}
        user = self.request.user
        if step == 'photos':
            initial_dict = {}
        elif step == 'person_data':
            profile_data = TherapistProfile.objects.filter(user=user).values(
                'gender',
                'birth_date',
                'height',
                'weight'
            ).first()
            if profile_data:
                initial_dict = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'gender': profile_data['gender'],
                    'height': profile_data['height'],
                    'weight': profile_data['weight'],
                }
                bd = profile_data['birth_date']
                if bd:
                    initial_dict['birth_date'] = bd.isoformat()
        elif step == 'therapist_data':
            profile_data = TherapistProfile.objects.filter(user=user).values(
                'practice_start_date',
                'massage_for',
            ).first()
            mf = TherapistProfile.objects.filter(user=user).values_list('massage_for', flat=True).all()
            if mf:
                initial_dict['massage_for'] = list(mf)
            if profile_data:
                psd = profile_data.get('practice_start_date')
                if psd:
                    initial_dict['practice_start_date'] = psd.isoformat()
            bs = BasicService.objects.get(pk=1)
            prices = BasicServicePrice.objects.filter(
                service=bs,
                specialist=TherapistProfile.objects.get(user=self.request.user)
            ).values('home_price', 'on_site_price').first()
            if prices:
                initial_dict.update(prices)
        elif step == 'contact_data':
            initial_dict = TherapistProfile.objects.filter(user=user).values(
                'address',
                'phone_number',
                'telegram_profile',
                'instagram_profile',
            ).first()
        elif step == 'about':
            description = TherapistProfile.objects.filter(user=user).values(
                'description',
            ).first()
            formatted_description = mark_safe(description['description'])
            initial_dict['description'] = formatted_description
        else:
            raise KeyError(f'Такой анкеты нет. Передано {step}, ожидается одно из {FORMS}')
        logging.debug(initial_dict)
        return initial_dict


class ProfileView(LoginRequiredMixin, DataMixin, TemplateView):
    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_therapist:
            return self.get_therapist_context_data(self, *args, **kwargs)
        else:
            return self.get_user_context_data(self, *args, **kwargs)

    def get_template_names(self):
        if self.request.user.is_therapist:
            return ['users/profile.html']
        else:
            return ['users/profile.html']

    def get_user_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}

    def get_therapist_context_data(self, *args, **kwargs):
        context = self.get_user_context(**kwargs)
        specialist = self.get_therapist()
        offers = Listing.objects.filter(therapist_id=specialist.pk)
        photos = Photo.objects.filter(user=specialist)
        ct = ContentType.objects.get_for_model(specialist)
        reviews = UserRating.objects.filter(rating__content_type=ct, rating__object_id=specialist.pk)
        is_reviewed = self.request.user in [review.user for review in reviews]
        review_form = self.get_review_form(specialist=specialist)
        context['is_reviewed'] = is_reviewed
        context['specialist'] = specialist
        context['content_type_id'] = ct.pk
        context['offers'] = offers
        context['all_photos'] = photos
        context['count'] = Bookmark.objects.filter(object_id=specialist.pk, content_type_id=ct.pk).count()
        context['is_bookmarked'] = Bookmark.objects.filter(content_type_id=ct.pk,
                                                           user_id=self.request.user.pk,
                                                           object_id=specialist.pk).exists()
        context['reviews'] = reviews
        context['review_form'] = review_form
        context['listings'] = specialist.listings.all()
        return context

    @staticmethod
    def get_review_form(specialist):
        review_form = ReviewForm()
        review_form.fields['review_for'].initial = specialist.pk
        return review_form

    def get_therapist(self):
        return self.request.user


class TherapistProfileDetailView(ProfileView):
    def get_therapist(self):
        therapist_name = self.kwargs.get('therapist_username')
        therapist = User.objects.get(username=therapist_name)
        return therapist

    def get_template_names(self):
        return ['users/profile.html']


class SpecialistsListView(DataMixin, FilterFormMixin, ListView):
    model = User
    paginate_by = 20
    template_name = 'users/specialists_list.html'
    context_object_name = 'specialists'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Специалисты')
        context['filter_form'] = TherapistFilterForm(initial=self.request.GET)
        context['content_type_id'] = ContentType.objects.get_for_model(User).pk
        return {**context, **context_def}

    def get_queryset(self):
        specialists = User.objects.annotate(
            min_price=F('therapist_profile__basicserviceprice__home_price'),
            # TODO: сейчас всегда берётся цена дома, нужно сделать чтобы выбиралась наименьшая из дома/на выезде
        )
        if self.request.user.is_authenticated:
            bookmarked_subquery = Bookmark.objects.filter(
                user=self.request.user,
                content_type=ContentType.objects.get_for_model(User),
                object_id=OuterRef('pk')
            ).values('user').annotate(is_bookmarked=Value(True, output_field=BooleanField())).values('is_bookmarked')

            # Получаем список пользователей с полем is_bookmarked
            specialists = specialists.annotate(
                is_bookmarked=Subquery(bookmarked_subquery, output_field=BooleanField())
            )
        form = TherapistFilterForm(self.request.GET)
        if form.is_valid():
            queryset = form.filter(specialists)
        else:
            logging.error(form.errors)
        return queryset


class TherapistOnMapListView(SpecialistsListView):
    template_name = 'users/specialists_on_map.html'
