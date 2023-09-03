from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView
from django.db.utils import IntegrityError

from feedback.forms import CommentForm, LikeForm
from feedback.models import Comment, LikeDislike, Bookmark
from listings.models import Listing
from users.models import *
from users.forms import TherapistProfileForm, UserProfileForm, TherapistFilterForm
from tantrakazan.utils import DataMixin, FilterFormMixin
from users.photo_processor import crop_face
from gallery.models import Gallery


class AddAvatar(LoginRequiredMixin, DataMixin, FormView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Добавление фото пользователя')
        return dict(list(context.items()) + list(context_def.items()))

    def get_success_url(self):
        if TherapistProfile.objects.filrer(user=self.request.user).exists():
            return reverse_lazy('users:create_therapist_profile')
        return reverse_lazy('users:user', kwargs={'username': self.request.user})

    def form_valid(self, form):
        user = self.request.user
        form.cleaned_data['user'] = user
        photo = self.request.FILES.get('avatar')
        cropped_photo = crop_face(uploaded_image=photo)
        user.avatar = cropped_photo
        user.save()
        return super().form_valid(form)


class AddUserAvatar(AddAvatar):

    def get_success_url(self):
        return reverse_lazy('users:user', kwargs={'username': self.request.user})


class AddTherapistAvatar(AddAvatar):

    def get_success_url(self):
        return reverse_lazy('users:create_therapist_profile')


class UserProfileCompletionView(LoginRequiredMixin, DataMixin, FormView):
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:therapist_profile')
    form_class = UserProfileForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Анкета')
        return dict(list(context.items()) + list(context_def.items()))

    def form_valid(self, form):
        photo = self.request.FILES.get('avatar')
        if photo:
            user = self.request.user
            cropped_photo = crop_face(uploaded_image=photo)
            user.avatar = cropped_photo
            user.save()
        return super().form_valid(form)


class TherapistProfileFormBaseView(UserProfileCompletionView):
    form_class = TherapistProfileForm

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data.pop('first_name', '')
        user.last_name = form.cleaned_data.pop('last_name', '')
        # tags = form.cleaned_data.pop('tags', None)
        tp, created = TherapistProfile.objects.update_or_create(user=user, defaults=form.cleaned_data)
        # tp.tags.set(tags)
        user.save()
        tp.save()
        return super().form_valid(form)


class TherapistProfileCompletionView(TherapistProfileFormBaseView):
    def form_valid(self, form):
        user = self.request.user
        user.is_therapist = True
        user.save()
        try:
            self.create_default_gallery()
        except IntegrityError:
            print('Галерея уже существует')
        return super().form_valid(form)

    def create_default_gallery(self):
        """Для всех пользователей создающих профиль массажиста создается
        галерея сертификатов и одна галерея фото"""
        user = self.request.user
        Gallery.objects.create(user=user,
                               slug=f'licenses',
                               title='Сертификаты',
                               description='Мои сертификаты')

        Gallery.objects.create(user=user,
                               slug=f'gallery',
                               title='Фото',
                               description='Мои фотографии')


class UserFormUpdateView(TherapistProfileFormBaseView):

    def get_context_data(self, *, object_list=None, **kwargs):
        initial = self.get_initial()
        form = TherapistProfileForm(initial=initial)
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context

    def get_initial(self):
        user = self.request.user
        user_data = {'first_name': user.first_name, 'last_name': user.last_name, 'avatar': user.avatar}
        profile_data = TherapistProfile.objects.filter(user=user).values(
            'gender',
            'birth_date',
            'height',
            'weight',
            'experience',
            'address',
            'show_address',
            'phone_number',
            'show_phone_number',
            'telegram_profile',
            'show_telegram_profile',
            'instagram_profile',
            'show_instagram_profile',
            'description',
            'is_profile_active'
        ).first()
        bd = profile_data['birth_date']
        if bd:
            profile_data['birth_date'] = bd.isoformat()
        return user_data | profile_data


class ProfileView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'users/user_profile_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}


class TherapistSelfProfileDetailView(ProfileView):
    template_name = 'users/therapist_self_profile_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
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
        context['content_type_id'] = content_type.pk
        context['offers'] = offers
        context['galleries'] = galleries
        context['count'] = Bookmark.objects.filter(object_id=therapist.pk, content_type_id=content_type.pk).count()
        context['is_bookmarked'] = Bookmark.objects.filter(content_type_id=content_type.pk, user_id=self.request.user.pk, object_id=therapist.pk).exists()
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


class TherapistProfileDetailView(TherapistSelfProfileDetailView):
    template_name = 'users/therapist_profile_detail.html'

    def get_therapist(self):
        therapist_name = self.kwargs.get('therapist_username')
        therapist = User.objects.get(username=therapist_name)
        return therapist


class TherapistListView(DataMixin, FilterFormMixin, ListView):
    model = User
    template_name = 'users/therapist_list.html'
    context_object_name = 'therapists'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Специалисты')
        filter_params, parameters = self.filter_parameters()
        context['filter_form'] = TherapistFilterForm(initial=parameters),
        return {**context, **context_def}

    def get_queryset(self):
        active_therapists = User.objects.with_comments_count()
        sorted_users = active_therapists.filter(ratings__isnull=False).order_by('-ratings__average')
        form = TherapistFilterForm(self.request.GET)
        if form.is_valid():
            queryset = form.filter(sorted_users)
        return queryset


class TherapistOnMapListView(TherapistListView):
    template_name = 'users/therapists_on_map.html'
