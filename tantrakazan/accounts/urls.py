from django.contrib.auth import views
from django.urls import path, reverse_lazy

from accounts.forms import UserPasswordResetForm, LoginUserForm, MyPasswordChangeForm
from accounts.views import RegisterUserCreateView, RegisterSpecialistCreateView, RegistrationDone, user_activate

app_name = 'accounts'

urlpatterns = [
    path("registration/", RegisterUserCreateView.as_view(), name="registration"),
    path("specialist_registration/", RegisterSpecialistCreateView.as_view(), name="specialist_registration"),
    path("registration/done", RegistrationDone.as_view(), name="registration_done"),
    path("registration/activate/<str:sign>", user_activate, name="register_activate"),
    path("login/", views.LoginView.as_view(template_name="accounts/login.html", form_class=LoginUserForm), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
                                        email_template_name="accounts/password_reset_email.html",
                                        success_url=reverse_lazy("accounts:password_reset_done"),
                                        form_class=UserPasswordResetForm),
        name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html', ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html",
                                               post_reset_login=True,
                                               success_url=reverse_lazy("users:profile")),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
