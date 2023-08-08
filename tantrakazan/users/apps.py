from django.apps import AppConfig
from django.dispatch import Signal
from users.utils import send_activation_notification


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'


user_registered = Signal()


def user_registered_dispatcher(instance, **kwargs):
    send_activation_notification(instance)


user_registered.connect(user_registered_dispatcher)
