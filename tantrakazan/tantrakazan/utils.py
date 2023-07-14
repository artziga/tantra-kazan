menu = [
    {'title': 'О нас', 'url_name': 'users:therapists'},
    {'title': 'Связаться', 'url_name': 'users:therapists'},
    {'title': 'Статьи', 'url_name': 'listings:listings'},
    {'title': 'Услуги', 'url_name': 'listings:listings'},
    {'title': 'Специалисты', 'url_name': 'users:therapists'},
    {'title': 'Главная', 'url_name': 'home'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context
