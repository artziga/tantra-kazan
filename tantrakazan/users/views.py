from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView
from django.db.utils import IntegrityError

from listings.models import Listing
from users.models import *
from users.forms import TherapistProfileForm, UserProfileForm
from tantrakazan.utils import DataMixin
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
        services = form.cleaned_data.pop('services', [])
        tp, created = TherapistProfile.objects.update_or_create(user=user, defaults=form.cleaned_data)
        tp.services.set(services)
        user.save()
        tp.save()
        return super().form_valid(form)


class TherapistProfileCompletionView(TherapistProfileFormBaseView):
    def form_valid(self, form):
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
                               slug=f'{user.username}s_licenses',
                               title='Сертификаты',
                               description='Мои сертификаты')

        Gallery.objects.create(user=user,
                               slug=f'{user.username}s_gallery',
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
        services = TherapistProfile.objects.get(user=user).services.values_list('pk', flat=True).all()
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
        profile_data['services'] = list(services)
        return user_data | profile_data


class ProfileView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'users/user_profile_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')
        return {**context, **context_def}


class TherapistProfileDetailView(ProfileView):
    template_name = 'users/therapist_profile_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        offers = Listing.objects.filter(therapist_id=user.pk)
        galleries = Gallery.objects.filter(user=user)
        samples = {gallery.title: gallery.sample(user=user, count=5) for gallery in galleries}
        context['offers'] = offers
        context['galleries'] = galleries
        context['samples'] = samples
        return context


class TherapistListView(DataMixin, ListView):
    model = User
    template_name = 'users/therapist_list.html'
    context_object_name = 'therapists'
    queryset = User.objects.filter(therapist_profile__is_profile_active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Профиль')

        return {**context, **context_def}
