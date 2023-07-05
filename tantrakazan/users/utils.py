

menu = [{'title': 'Сгенерировать меню', 'url_name': 'collect_user_data'},
        {'title': 'Показать меню', 'url_name': 'show_menu'},
        {'title': 'Рецепты', 'url_name': 'dishes'},
        {'title': 'Категории', 'url_name': 'cats'},
        {'title': 'Ингридиенты', 'url_name': 'ingredients'},
        {'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Контакты', 'url_name': 'contacts'}
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        return context