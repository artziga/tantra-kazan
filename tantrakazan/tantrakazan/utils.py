from users.models import TherapistProfile

menu = [
    {'title': 'Связаться', 'url_name': 'users:therapists'},
    {'title': 'Статьи', 'url_name': 'listings:listings'},
    {'title': 'Услуги', 'url_name': 'listings:listings'},
    {'title': 'Специалисты', 'url_name': 'users:therapists'},
    {'title': 'Главная', 'url_name': 'main:home'},
]


class DataMixin:

    def get_user_context(self, **kwargs):
        user_menu = menu.copy()
        user = self.request.user
        create_therapist_profile_button = {
                    'title': 'Зарегестрироваться как массажист',
                    }
        if user.is_authenticated:
            if not TherapistProfile.objects.filter(user=user).exists():
                create_therapist_profile_button['url_name'] = 'users:add_therapist_avatar'
                user_menu.insert(0, create_therapist_profile_button)
        else:
            create_therapist_profile_button['url_name'] = 'users:therapist_registration'
            user_menu.insert(0, create_therapist_profile_button)
        context = kwargs
        context['menu'] = user_menu
        return context
