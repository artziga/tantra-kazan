from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView
from django.db.utils import IntegrityError
from formtools.wizard.views import SessionWizardView
import logging

from feedback.forms import CommentForm, LikeForm
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
                         OrderingForm)
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


def test(request):
    return render(request, 'users/test.html', context={'one': FORMS_NAMES})


def make_user_a_therapist(user):
    user.is_therapist = True
    user.save()
    TherapistProfile.objects.create(user=user)
    Gallery.objects.create(user=user, title='Мои сертификаты')
    Gallery.objects.create(user=user, title='Мои фото')


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
            return ['users/therapist_self_profile_detail.html']
        else:
            return ['users/user_profile_detail.html']

    def get_user_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}

    def get_therapist_context_data(self, *args, **kwargs):
        context = self.get_user_context(**kwargs)
        therapist = self.get_therapist()
        offers = Listing.objects.filter(therapist_id=therapist.pk)
        galleries = Gallery.objects.filter(user=therapist)
        content_type = ContentType.objects.get_for_model(therapist)
        comments = Comment.objects.filter(
            content_type=content_type,
            object_id=therapist.pk
        )
        like_to_therapist_form = self.get_like_form(content_type=content_type, therapist=therapist)
        comment_form = self.get_comment_form(content_type=content_type, therapist=therapist)
        context['therapist'] = therapist
        logging.info(therapist)
        context['content_type_id'] = content_type.pk
        context['offers'] = offers
        context['galleries'] = galleries
        context['count'] = Bookmark.objects.filter(object_id=therapist.pk, content_type_id=content_type.pk).count()
        context['is_bookmarked'] = Bookmark.objects.filter(content_type_id=content_type.pk,
                                                           user_id=self.request.user.pk,
                                                           object_id=therapist.pk).exists()
        context['comments'] = comments
        context['like_to_therapist_form'] = like_to_therapist_form
        context['comment_form'] = comment_form
        return context

    @staticmethod
    def get_comment_form(content_type, therapist):
        comment_form = CommentForm()
        comment_form.fields['content_type'].initial = content_type
        comment_form.fields['object_id'].initial = therapist.pk
        return comment_form

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
        return ['users/therapist_profile_detail.html']


class SpecialistsListView(DataMixin, FilterFormMixin, ListView):
    model = User
    paginate_by = 20
    template_name = 'users/specialists_list.html'
    context_object_name = 'specialists'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Специалисты')
        filter_params, parameters = self.filter_parameters()
        context['filter_form'] = TherapistFilterForm()
        context['ordering_form'] = OrderingForm(initial={'order_by': '-age'})
        context['content_type_id'] = ContentType.objects.get_for_model(User).pk
        return {**context, **context_def}

    def get_queryset(self):
        specialists = User.objects.with_comments_count()
        sorted_users = specialists.filter(ratings__isnull=False).order_by('-ratings__average')

        print(specialists.values('ratings__average').all())
        form = TherapistFilterForm(self.request.GET)
        if form.is_valid():
            queryset = form.filter(sorted_users)
        return sorted_users


class TherapistOnMapListView(SpecialistsListView):
    template_name = 'users/specialists_on_map.html'
