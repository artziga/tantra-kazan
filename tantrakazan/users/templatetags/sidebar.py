from django import template
from django.urls import reverse_lazy

register = template.Library()


@register.inclusion_tag('users/sidebar.html')
def sidebar(user, selected):
    menu = {
        user.username: reverse_lazy('users:profile'),
        'Избранное': reverse_lazy('users:favorite'),
        'Редактировать профиль': reverse_lazy('users:edit_profile', kwargs={'pk': user.pk}),
        'Сменить пароль': reverse_lazy('users:change_password'),
        'Выйти': reverse_lazy('accounts:logout')
    }
    return {
        'menu': menu,
        'current': selected
        }
