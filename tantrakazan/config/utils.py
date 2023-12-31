from dal import autocomplete
from django.db.models import Count
from geopy import Yandex
from geopy import Point
from taggit.models import Tag
from gallery.models import Photo

from config.settings import YANDEX_GEOCODER_API_KEY as API_KEY, YANDEX_GEOSUGGEST_API_KEY as GEOSUGGEST_KEY

menu = [
    {'title': 'Связаться', 'url_name': 'users:specialist'},
    {'title': 'Статьи', 'url_name': 'listings:listings'},
    {'title': 'Услуги', 'url_name': 'listings:listings'},
    {'title': 'Мастера', 'url_name': 'users:specialist'},
    {'title': 'Главная', 'url_name': 'main:home'},
]


class DataMixin:
    title = None

    def get_user_context(self, **kwargs):
        user_menu = menu.copy()
        user = self.request.user
        create_specialist_profile_button = {
            'title': 'Зарегестрироваться как массажист',
        }
        if user.is_authenticated:
            if not user.is_specialist:
                create_specialist_profile_button['url_name'] = 'users:become_a_specialist'
                user_menu.insert(0, create_specialist_profile_button)
        else:
            create_specialist_profile_button['url_name'] = 'accounts:specialist_registration'
            user_menu.insert(0, create_specialist_profile_button)
        context = kwargs
        context['menu'] = user_menu
        context['API_KEY'] = API_KEY
        context['GEOSUGGEST_KEY'] = GEOSUGGEST_KEY
        if user.is_authenticated:
            context['avatar'] = Photo.objects.filter(user=user, is_avatar=True).first()
        if self.title:
            context['title'] = self.title
        return context


class Locator:

    def __init__(self, raw_place: str = None):
        self.place = raw_place

    def location(self, place=None):
        if place is None:
            place = self.place
        return Yandex(api_key=API_KEY).geocode(place)


class FilterFormMixin:
    """Готовит набор параметров фильтрации переданных
    в форме фильтрации для добавления в GET запрос"""

    def get_filled_filter_parameters(self):
        filter_parameters = {}
        get_dict = self.request.GET
        for parameter in get_dict:
            if get_dict[parameter]:
                # if parameter == 'categories':
                #     filter_parameters['categories'] = get_dict.getlist('categories')
                # else:
                filter_parameters[parameter] = get_dict[parameter]
        return filter_parameters

    def filter_parameters(self):
        parameters_for_url = self.request.GET.copy()
        if 'page' in parameters_for_url:
            del parameters_for_url['page']
        filled_parameters = self.get_filled_filter_parameters()
        return parameters_for_url, filled_parameters


# class TagAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         qs = Tag.objects.annotate(total_count=Count('article') + Count('listing'))
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#
#         return qs.order_by('-total_count')[:5]

