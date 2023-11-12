from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from accounts.apps import user_registered
from accounts.forms import RegisterUserForm, MySetPasswordForm
from main.models import User
from tantrakazan.utils import DataMixin
from accounts.utils import signer
from specialists.views import make_user_a_specialist


class RegisterUserCreateView(DataMixin, CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('accounts:registration_done')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(context_def.items()))

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user_registered.send(sender=self.__class__, instance=user)
        return response


class RegisterSpecialistCreateView(RegisterUserCreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        make_user_a_specialist(user)
        return response


class RegistrationDone(DataMixin, TemplateView):
    template_name = 'accounts/registration_done.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Регистрация')
        return {**context, **context_def}


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'accounts/bad_signature.html', {'title': 'Активация не удалась'})

    user = get_object_or_404(User, username=username)
    if user.is_active:
        template = 'accounts/user_is_activated.html'
        return render(request, template, {'title': 'Активация выполнена ранее'})

    user.is_active = True
    user.is_activated = True
    user.save()
    login(request, user)
    goto = 'users:edit_profile' if user.is_therapist else 'users:profile'
    return redirect(goto)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = MySetPasswordForm
    post_reset_login = True

    def get_success_url(self):
        return reverse_lazy("specialists:profile") if self.request.user.is_therapist else reverse_lazy("users:profile")
