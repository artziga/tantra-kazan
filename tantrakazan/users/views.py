from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Case, Q, F, When, PositiveSmallIntegerField, OuterRef, Value, BooleanField, Subquery
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView
from django.db.utils import IntegrityError
from formtools.wizard.views import SessionWizardView
import logging

from star_ratings.models import UserRating

from feedback.forms import ReviewForm, LikeForm
from feedback.models import LikeDislike, Bookmark
from listings.models import Listing
from users.models import *
from main.models import User
from users.forms import (TherapistProfileForm,
                         CreateAvatarForm,
                         PersonDataForm,
                         TherapistDataForm,
                         ContactDataForm,
                         AboutForm,
                         ActivateProfileForm,
                         TherapistFilterForm,
                         )
from tantrakazan.utils import DataMixin, FilterFormMixin
from gallery.photo_processor import CropFace
from gallery.models import Gallery, Avatar

FORMS = [("person_data", PersonDataForm),
         ("therapist_data", TherapistDataForm),
         ("contact_data", ContactDataForm),
         ("about", AboutForm)
         ]

FORMS_NAMES = ["Общие данные",
               "Профессиональные данные",
               "Контактные данные",
               "О себе"]



def make_user_a_therapist(user):
    user.is_therapist = True
    user.save()
    TherapistProfile.objects.create(user=user)
    Gallery.objects.create(user=user, title='Галерея', slug='gallery')


@login_required
def become_a_therapist(request):
    return render(request, template_name='users/become_a_therapist_confirmation.html')


def become_a_therapist_confirmation(request):
    user = request.user
    make_user_a_therapist(user)
    return redirect('users:add_avatar')


class AddAvatar(LoginRequiredMixin, DataMixin, FormView):
    model = Avatar
    form_class = CreateAvatarForm
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
            users_avatar = Avatar.objects.create(image=photo)
            user.avatar = users_avatar
            user.save()
        return super().form_valid(form)


class TherapistProfileWizard(LoginRequiredMixin, DataMixin, SessionWizardView):
    form_list = FORMS
    template_name = 'users/wizard_form.html'

    def done(self, form_list, **kwargs):
        cleaned_data = self.get_all_cleaned_data()
        user = self.request.user
        user.first_name = cleaned_data.pop('first_name', '')
        user.last_name = cleaned_data.pop('last_name', '')
        tp, created = TherapistProfile.objects.update_or_create(user=user, defaults=cleaned_data)
        user.save()
        tp.save()
        logging.info("Wizard is done")
        return redirect('users:profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Анкета')
        context['steps'] = FORMS_NAMES
        return dict(list(context.items()) + list(context_def.items()))

    def get_form_initial(self, step):
        initial_dict = {}
        user = self.request.user
        if step == 'person_data':
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
                'experience',
                'massage_to_male',
                'massage_to_female'
            ).first()
            logging.info(profile_data)
            if profile_data:
                if profile_data['massage_to_male'] is not True:
                    massage_to_male_or_female = False
                elif profile_data['massage_to_female'] is not True:
                    massage_to_male_or_female = True
                else:
                    massage_to_male_or_female = None
                initial_dict = {'experience': profile_data['experience'],
                                'massage_to_male_or_female': massage_to_male_or_female}
        elif step == 'contact_data':
            initial_dict = TherapistProfile.objects.filter(user=user).values(
                'address',
                'show_address',
                'phone_number',
                'show_phone_number',
                'telegram_profile',
                'show_telegram_profile',
                'instagram_profile',
                'show_instagram_profile',
            ).first()
        elif step == 'about':
            initial_dict = TherapistProfile.objects.filter(user=user).values(
                'short_description',
                'description',
            ).first()
        else:
            raise KeyError(f'Такой анкеты нет. Передано {step}, ожидается одно из {FORMS}')
        logging.info(initial_dict)
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
        gallery = Gallery.objects.filter(user=specialist).first()
        avatar = specialist.avatar
        photos = gallery.photos.all()
        all_photos = [avatar] + list(photos)
        ct = ContentType.objects.get_for_model(specialist)
        reviews = UserRating.objects.filter(rating__content_type=ct, rating__object_id=specialist.pk)
        like_to_therapist_form = self.get_like_form(content_type=ct, therapist=specialist)
        review_form = self.get_review_form(specialist=specialist)
        context['specialist'] = specialist
        context['content_type_id'] = ct.pk
        context['offers'] = offers
        context['all_photos'] = all_photos
        context['count'] = Bookmark.objects.filter(object_id=specialist.pk, content_type_id=ct.pk).count()
        context['is_bookmarked'] = Bookmark.objects.filter(content_type_id=ct.pk,
                                                           user_id=self.request.user.pk,
                                                           object_id=specialist.pk).exists()
        context['reviews'] = reviews
        context['like_to_therapist_form'] = like_to_therapist_form
        context['review_form'] = review_form
        context['listings'] = specialist.listings.all()
        return context

    @staticmethod
    def get_review_form(specialist):
        review_form = ReviewForm()
        review_form.fields['review_for'].initial = specialist.pk
        return review_form

    def get_like_form(self, content_type, therapist):
        like_form = LikeForm()
        try:
            like_or_dislike = LikeDislike.objects.get(
                user=self.request.user,
                object_id=therapist.pk,
                content_type=content_type
            )
            like_form.fields['like_or_dislike'].initial = like_or_dislike.like_or_dislike
        except LikeDislike.DoesNotExist:
            like_form.fields['like_or_dislike'].initial = None
        like_form.fields['content_type'].initial = content_type
        like_form.fields['object_id'].initial = therapist.pk
        return like_form

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
            min_price=F('therapist_profile__basicserviceprice__home_price'), #TODO: сейчас всегда берётся цена дома, нужно сделать чтобы выбиралась наименьшая из дома/на выезде
            )
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
