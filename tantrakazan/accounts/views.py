from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, LoginView, PasswordChangeView
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from accounts.apps import user_registered
from accounts.forms import RegisterUserForm, MySetPasswordForm, LoginUserForm, MyPasswordChangeForm
from config.utils import DataMixin
from accounts.utils import signer
from specialists.utils import make_user_a_specialist

User = get_user_model()


class MyLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy('specialists:profile') if self.request.user.is_specialist else reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_label'] = 'Вход'
        context['title'] = 'Вход'
        return context


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
    goto = 'users:edit_profile' if user.is_specialist else 'users:profile'
    return redirect(goto)


class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy("accounts:password_change_done")
    form_class = MyPasswordChangeForm


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = MySetPasswordForm
    post_reset_login = True

    def get_success_url(self):
        return reverse_lazy("specialists:profile") if self.request.user.is_specialist else reverse_lazy("users:profile")
